in part (.sldprt) file run "add part number and name to cutlist items.swp" macro file

to extract DXFs run "Extract_DXFs.swp" macro file on either part (.sldprt) or assembly (.sldasm) file. Make sure to entre default ("D:\Dxf Location") save folder location in the macro code.

extract BOM of DXFs. Note excel sould not contains '\t', and '\n' in part number or sheet metal thickness.

run python do segrgate DXFs based on their thickness, make sure to enter location of DXFs folder, BOM excel, and save folder.

