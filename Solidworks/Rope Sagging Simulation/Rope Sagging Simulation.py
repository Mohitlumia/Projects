"""
Rope loop simulation (mm coordinate system)
- Units: world coordinates are in millimetres (mm)
- Display: everything converted to pixels via origin and scale (px_per_mm)

Controls:
 - + : add one segment at mouse
 - - : remove nearest node at mouse
 - Left mouse drag on circle: move (circle collides with rope)
 - Right mouse drag on circle: move (circle ignored by rope while dragging)
 - Left mouse drag on node: pinch/move rope node
 - S : save simulation (simulation_save_mm.json) in mm
 - L : load simulation
 - O : set origin to current mouse position (sets screen pixel -> world mm mapping)
 - [ / ] : decrease / increase scale (pixels per mm)
 - ESC : quit

Run: requires pygame and numpy
    pip install pygame numpy
    python rope_loop_mm_simulation.py

File saves node and circle positions in mm so you can reload later.
"""

import pygame
import numpy as np
import json
import os

# -------------------- Units & coordinate system --------------------
# World: millimetres (mm)
# Screen: pixels (px)

DEFAULT_PX_PER_MM = 2.0    # pixels per millimetre
DEFAULT_ORIGIN_PX = np.array([50.0, 450.0])  # screen pixel coords where world (0,0) mm sits

# convert functions (vectorized)

def to_px(vec_mm, origin_px, px_per_mm):
    """Convert mm -> screen px (Y positive up)"""
    return np.array([
        origin_px[0] + vec_mm[0] * px_per_mm,
        origin_px[1] - vec_mm[1] * px_per_mm   # minus here flips Y
    ])

def to_mm(vec_px, origin_px, px_per_mm):
    """Convert screen px -> mm (Y positive up)"""
    return np.array([
        (vec_px[0] - origin_px[0]) / px_per_mm,
        -(vec_px[1] - origin_px[1]) / px_per_mm  # minus here flips Y
    ])


# -------------------- Node, Circle, Rope --------------------
class Node:
    def __init__(self, pos_mm):
        # store positions in mm
        self.pos = np.array(pos_mm, dtype=float)
        self.old_pos = np.array(pos_mm, dtype=float)


class CircleObstacle:
    def __init__(self, pos_mm, radius_mm):
        self.pos = np.array(pos_mm, dtype=float)   # mm
        self.radius = float(radius_mm)             # mm
        self.dragging = False
        self.ignore_collision = False

    def handle_event(self, event, sim):
        mouse_px = np.array(pygame.mouse.get_pos(), dtype=float)
        mouse_mm = to_mm(mouse_px, sim.origin_px, sim.px_per_mm)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if np.linalg.norm(mouse_mm - self.pos) <= self.radius:
                if event.button == 1:  # left click -> colliding drag
                    self.dragging = True
                    self.ignore_collision = False
                elif event.button == 3:  # right click -> ghost drag
                    self.dragging = True
                    self.ignore_collision = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button in (1, 3):
                self.dragging = False
                self.ignore_collision = False

    def update(self, sim):
        if self.dragging:
            mouse_px = np.array(pygame.mouse.get_pos(), dtype=float)
            self.pos = to_mm(mouse_px, sim.origin_px, sim.px_per_mm)

    def draw(self, screen, sim):
        # draw in pixels
        p = to_px(self.pos, sim.origin_px, sim.px_per_mm)
        r = int(round(self.radius * sim.px_per_mm))
        color = (200, 100, 100) if not self.ignore_collision else (140, 140, 140)
        pygame.draw.circle(screen, color, p.astype(int), max(1, r))
        pygame.draw.circle(screen, (255, 200, 200), p.astype(int), max(1, r), 2)


class Rope:
    def __init__(self, center_mm, num_nodes=36, seg_length_mm=15.0):
        self.center = np.array(center_mm, dtype=float)
        self.seg_length = float(seg_length_mm)  # mm per segment
        self.nodes = []
        self._build_circle(num_nodes)
        self.dragging_node = None

    def _build_circle(self, num_nodes):
        circumference = num_nodes * self.seg_length
        radius = circumference / (2.0 * np.pi)
        angles = np.linspace(0, 2 * np.pi, num_nodes, endpoint=False)
        self.nodes = [Node(self.center + radius * np.array([np.cos(a), np.sin(a)])) for a in angles]

    @property
    def num_nodes(self):
        return len(self.nodes)

    def apply_forces(self, g_mm_s2=-981.0, dt=0.016, damping=0.995):
        # Verlet integration in mm units
        for n in self.nodes:
            vel = (n.pos - n.old_pos) * damping
            n.old_pos = n.pos.copy()
            n.pos = n.pos + vel + np.array([0.0, g_mm_s2]) * (dt * dt)

    def satisfy_constraints(self, iterations=20, circles=None):
        if circles is None:
            circles = []
        N = self.num_nodes
        for _ in range(iterations):
            # distance constraints (closed loop)
            for i in range(N):
                j = (i + 1) % N
                n1 = self.nodes[i]
                n2 = self.nodes[j]
                d = n2.pos - n1.pos
                dist = np.linalg.norm(d)
                if dist == 0.0:
                    d = np.array([1e-6, 0.0])
                    dist = np.linalg.norm(d)
                diff = (dist - self.seg_length) / dist
                correction = 0.5 * diff * d
                n1.pos += correction
                n2.pos -= correction

            # circle collisions (project nodes outside circles)
            for n in self.nodes:
                for c in circles:
                    if c.ignore_collision:
                        continue
                    v = n.pos - c.pos
                    d = np.linalg.norm(v)
                    if d == 0.0:
                        v = np.array([1e-3, 0.0])
                        d = np.linalg.norm(v)
                    if d < c.radius:
                        n.pos = c.pos + (v / d) * c.radius

    def draw(self, screen, sim):
        pts = [to_px(n.pos, sim.origin_px, sim.px_per_mm) for n in self.nodes]
        for i in range(self.num_nodes):
            j = (i + 1) % self.num_nodes
            pygame.draw.line(screen, (220, 220, 220), pts[i], pts[j], 3)
        for p in pts:
            pygame.draw.circle(screen, (100, 200, 255), p.astype(int), 3)

    # ---- Natural Add / Remove ----
    def add_segment_at_mouse(self, mouse_px, sim, count=1):
        for _ in range(count):
            if self.num_nodes < 3:
                continue
            mouse_mm = to_mm(mouse_px, sim.origin_px, sim.px_per_mm)
            best_dist = float('inf')
            best_proj = None
            best_i = 0
            for i in range(self.num_nodes):
                a = self.nodes[i].pos
                b = self.nodes[(i + 1) % self.num_nodes].pos
                dist, proj = point_segment_distance(mouse_mm, a, b)
                if dist < best_dist:
                    best_dist = dist
                    best_proj = proj
                    best_i = i
            insert_index = best_i + 1
            self.nodes.insert(insert_index, Node(best_proj))
            # note: seg_length constant => total loop length increases by seg_length

    def remove_node_nearest(self, mouse_px, sim, count=1):
        for _ in range(count):
            if self.num_nodes <= 8:
                break
            mouse_mm = to_mm(mouse_px, sim.origin_px, sim.px_per_mm)
            dists = [np.linalg.norm(n.pos - mouse_mm) for n in self.nodes]
            idx = int(np.argmin(dists))
            if self.num_nodes > 8:
                self.nodes.pop(idx)

    # ---- Node dragging ----
    def handle_event(self, event, sim):
        mouse_px = np.array(pygame.mouse.get_pos(), dtype=float)
        mouse_mm = to_mm(mouse_px, sim.origin_px, sim.px_per_mm)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # find closest node within threshold (in mm)
            click_thresh_mm = 8.0  # mm
            dists = [np.linalg.norm(n.pos - mouse_mm) for n in self.nodes]
            idx = int(np.argmin(dists))
            if dists[idx] < click_thresh_mm:
                self.dragging_node = idx
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_node = None

    def update_dragging(self, sim):
        if self.dragging_node is not None:
            mouse_px = np.array(pygame.mouse.get_pos(), dtype=float)
            mouse_mm = to_mm(mouse_px, sim.origin_px, sim.px_per_mm)
            n = self.nodes[self.dragging_node]
            n.pos = mouse_mm.copy()
            n.old_pos = mouse_mm.copy()

# ---------- Utility: point to segment (mm) ----------

def point_segment_distance(p, a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    p = np.array(p, dtype=float)
    ab = b - a
    ab2 = np.dot(ab, ab)
    if ab2 == 0.0:
        return np.linalg.norm(p - a), a.copy()
    t = np.dot(p - a, ab) / ab2
    t_clamped = max(0.0, min(1.0, t))
    proj = a + t_clamped * ab
    return np.linalg.norm(p - proj), proj

# ---------- Simulation ----------
SAVE_FILE = "Rope hanging problem\Rope simulation\simulation_save_mm.json"

class Simulation:
    def __init__(self):
        pygame.init()
        self.W, self.H = 1000, 600
        self.screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("Rope loop (mm coords)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Consolas", 16)

        # world-to-screen transform
        self.px_per_mm = DEFAULT_PX_PER_MM
        self.origin_px = DEFAULT_ORIGIN_PX.copy()  # where world (0,0) sits on screen

        # simulation objects
        self.rope = Rope(center_mm=(750, 450), num_nodes=300, seg_length_mm=25)
        self.circles = [CircleObstacle((0, 0), 62.5),
                        CircleObstacle((1598, 906), 82.5),
                        ]


        self.running = True

    # ---- save/load ----
    def save_state(self, filename=SAVE_FILE):
        data = {
            "meta": {
                "px_per_mm": self.px_per_mm,
                "origin_px": self.origin_px.tolist()
            },
            "rope": {
                "seg_length_mm": self.rope.seg_length,
                "nodes_mm": [n.pos.tolist() for n in self.rope.nodes]
            },
            "circles": [{"pos_mm": c.pos.tolist(), "radius_mm": c.radius} for c in self.circles]
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved -> {filename}")

    def load_state(self, filename=SAVE_FILE):
        if not os.path.exists(filename):
            print("No save file found")
            return
        with open(filename, "r") as f:
            data = json.load(f)
        meta = data.get("meta", {})
        self.px_per_mm = meta.get("px_per_mm", self.px_per_mm)
        self.origin_px = np.array(meta.get("origin_px", self.origin_px.tolist()), dtype=float)
        r = data["rope"]
        self.rope.seg_length = r.get("seg_length_mm", self.rope.seg_length)
        self.rope.nodes = [Node(np.array(p)) for p in r.get("nodes_mm", [])]
        self.circles = [CircleObstacle(tuple(c["pos_mm"]), c["radius_mm"]) for c in data.get("circles", [])]
        print(f"Loaded <- {filename}")

    # ---- UI drawing helpers ----
    def draw_axes(self):
        # draw x/y axes based on origin_px and scale. ticks every 50 mm
        tick_mm = 50.0
        width_px, height_px = self.W, self.H
        # vertical ticks along X axis
        left_mm = to_mm(np.array([0.0, 0.0]), self.origin_px, self.px_per_mm)[0]
        right_mm = to_mm(np.array([width_px, 0.0]), self.origin_px, self.px_per_mm)[0]
        top_mm = to_mm(np.array([0.0, 0.0]), self.origin_px, self.px_per_mm)[1]
        bottom_mm = to_mm(np.array([0.0, height_px]), self.origin_px, self.px_per_mm)[1]

        # vertical grid lines (x constant)
        start_x = int(np.floor(left_mm / tick_mm) * tick_mm)
        end_x = int(np.ceil(right_mm / tick_mm) * tick_mm)
        for xm in np.arange(start_x, end_x + 0.1, tick_mm):
            px = to_px((xm, 0.0), self.origin_px, self.px_per_mm)[0]
            pygame.draw.line(self.screen, (40, 40, 40), (px, 0), (px, self.H), 1)
            label = f"{int(xm)} mm"
            surf = self.font.render(label, True, (100, 100, 100))
            self.screen.blit(surf, (px + 4, 4))

        # horizontal grid lines (y constant)
        start_y = int(np.floor(top_mm / tick_mm) * tick_mm)
        end_y = int(np.ceil(bottom_mm / tick_mm) * tick_mm)
        for ym in np.arange(start_y, end_y + 0.1, tick_mm):
            py = to_px((0.0, ym), self.origin_px, self.px_per_mm)[1]
            pygame.draw.line(self.screen, (40, 40, 40), (0, py), (self.W, py), 1)
            label = f"{int(ym)} mm"
            surf = self.font.render(label, True, (100, 100, 100))
            self.screen.blit(surf, (4, py + 2))

    def draw_info(self):
        lines = [
            "Controls: + add seg | - remove seg | S save | L load | O set origin",
            "Left-drag circle: collides   Right-drag: ghost (no collision)",
            "Left-drag near node: pinch rope",
            f"Scale: {self.px_per_mm:.2f} px/mm   Origin (px): {self.origin_px.astype(int).tolist()}"
        ]
        for i, s in enumerate(lines):
            surf = self.font.render(s, True, (230, 230, 230))
            self.screen.blit(surf, (10, 10 + i * 18))

        # mouse world coords
        mouse_px = np.array(pygame.mouse.get_pos(), dtype=float)
        mouse_mm = to_mm(mouse_px, self.origin_px, self.px_per_mm)
        coord_text = f"Mouse: {mouse_mm[0]:.1f} mm, {mouse_mm[1]:.1f} mm"
        surf = self.font.render(coord_text, True, (200, 200, 120))
        self.screen.blit(surf, (10, self.H - 30))

        # circle info
        for idx, c in enumerate(self.circles):
            text = f"Circle {idx+1}: x={c.pos[0]:.1f} mm, y={c.pos[1]:.1f} mm, d={2*c.radius:.1f} mm"
            surf = self.font.render(text, True, (200, 200, 120))
            self.screen.blit(surf, (10, 100 + idx * 18))

    # ---- main loop ----
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                        self.rope.add_segment_at_mouse(pygame.mouse.get_pos(), self, count=1)
                    elif event.key == pygame.K_MINUS:
                        self.rope.remove_node_nearest(pygame.mouse.get_pos(), self, count=1)
                    elif event.key == pygame.K_s:
                        self.save_state()
                    elif event.key == pygame.K_l:
                        self.load_state()
                    elif event.key == pygame.K_o:
                        # set origin to mouse position
                        self.origin_px = np.array(pygame.mouse.get_pos(), dtype=float)
                    elif event.key == pygame.K_LEFTBRACKET:
                        self.px_per_mm = max(0.1, self.px_per_mm - 0.1)
                    elif event.key == pygame.K_RIGHTBRACKET:
                        self.px_per_mm = min(20.0, self.px_per_mm + 0.1)

                # forward to rope for node-pinch
                self.rope.handle_event(event, self)
                # forward to circles
                for c in self.circles:
                    c.handle_event(event, self)

            # update
            for c in self.circles:
                c.update(self)
            self.rope.apply_forces()
            self.rope.update_dragging(self)
            self.rope.satisfy_constraints(iterations=12, circles=self.circles)

            # draw
            self.screen.fill((18, 18, 18))
            self.draw_axes()
            self.rope.draw(self.screen, self)
            for c in self.circles:
                c.draw(self.screen, self)
            self.draw_info()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    Simulation().run()
