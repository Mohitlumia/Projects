import os
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.properties import Properties
import matplotlib.pyplot as plt

# ---- Custom Frontend to force black lines ----
class BlackFrontend(Frontend):
    def override_properties(self, entity, properties: Properties) -> None:
        # Force all entities to be solid black
        properties.color = "#000000ff"  # RGBA hex: black, opaque


def save_dxf_as_png(dxf_path, png_path, dpi_=50):
    # Load DXF
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()

    # White background
    bg_color = "white"

    # Create figure + axes with white background
    fig, ax = plt.subplots()
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Render DXF with our custom frontend
    ctx = RenderContext(doc)
    backend = MatplotlibBackend(ax)

    BlackFrontend(ctx, backend).draw_layout(msp, finalize=True)

    # Adjust view
    ax.set_aspect("equal")
    ax.autoscale()
    ax.axis("off")

    # Save PNG
    fig.savefig(
        png_path,
        dpi=dpi_,
        facecolor=bg_color,
        bbox_inches="tight",
        pad_inches=0,
    )

    plt.close(fig)
