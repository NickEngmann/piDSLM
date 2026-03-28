# 3D Printing Guide

This guide provides instructions for printing the piDSLM enclosure.

## Quick Start

1. Print the main enclosure parts (see part list below)
2. Assemble using provided screws and magnets
3. Install Raspberry Pi, camera, and display
4. Attach optional grip modules

## Part List

### Required Parts

| Part | Quantity | Print Time | Material |
|------|----------|------------|----------|
| main_body.stl | 1 | 4-6 hours | PLA/PETG |
| top_cover.stl | 1 | 2-3 hours | PLA/PETG |
| side_panel.stl | 1 | 2-3 hours | PLA/PETG |

### Optional Parts

| Part | Quantity | Print Time | Material |
|------|----------|------------|----------|
| grip_standard.stl | 1 | 1-2 hours | PLA/PETG |
| grip_horizontal.stl | 1 | 1-2 hours | PLA/PETG |
| tripod_mount.stl | 1 | 30 min | PLA/PETG |

## Print Settings

### Base Settings
- **Layer Height**: 0.2mm
- **Infill**: 20% (structural parts), 10% (decorative)
- **Wall Thickness**: 2.4mm (3 walls)
- **Top/Bottom Layers**: 4 layers

### Recommended Materials
- **PLA**: Easiest to print, good for first attempts
- **PETG**: More durable, better heat resistance
- **ABS**: Best for outdoor use, requires enclosure

## Assembly Instructions

### 1. Print All Parts
Print all required parts before assembly.

### 2. Prepare Magnets
Heat magnets to ~60°C and press into designated slots in main_body.stl.

### 3. Assemble Enclosure
1. Place Raspberry Pi into main body
2. Connect camera ribbon cable
3. Attach top cover (snaps into place)
4. Insert magnets to secure camera module
5. Screw side panel into place

### 4. Attach Grip (Optional)
Snap grip module into place using magnetic attachment.

### 5. Install Display
Connect display to GPIO headers through side panel opening.

## Troubleshooting

### Parts Won't Fit
- Ensure print scale is 100%
- Check layer height consistency
- Slight sanding may be needed for tight fits

### Weak Magnet Hold
- Use stronger N52 grade magnets
- Ensure magnet slots are fully printed
- Add adhesive to magnet retention

### Cable Too Short
- Consider extending ribbon cables
- Use flexible flat cables
- Re-route through cable channels

## Tips

- Print in multiple colors for aesthetic appeal
- Leave magnet slots open for easier insertion
- Use PETG for parts exposed to heat
- Seal exterior with matte clear coat

---

For design modifications, see [DESIGN_IMPROVEMENTS.md](../DESIGN_IMPROVEMENTS.md)
