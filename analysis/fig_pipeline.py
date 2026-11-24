"""Writes media/pipeline.svg: BioArmband -> UDPSender.py -> UDP -> UDPReceiver.cs -> Unity object."""
from common import MEDIA

boxes = [
    ("BioArmband", "IMU quaternion\n[w,x,y,z]", 20),
    ("UDPSender.py", "normalise, send\nat 20 Hz", 215),
    ("UDP :9050", "\"a,b,c,d\" text\nover Wi-Fi", 410),
    ("UDPReceiver.cs", "parse, remap axes,\nset rotation", 605),
    ("Unity scene", "test object now,\nhand root next", 800),
]
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="980" height="150" viewBox="0 0 980 150" role="img" '
       'aria-label="Data path from the BioArmband to a Unity object over UDP">',
       '<rect width="980" height="150" rx="10" fill="#f6f7f9"/>',
       '<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
       '<path d="M0,0 L8,4 L0,8 z" fill="#333"/></marker></defs>']
for i, (title, sub, x) in enumerate(boxes):
    out.append(f'<rect x="{x}" y="35" width="160" height="80" rx="8" fill="#fff" stroke="#0072B2" stroke-width="2"/>')
    out.append(f'<text x="{x+80}" y="62" text-anchor="middle" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222">{title}</text>')
    for j, line in enumerate(sub.split("\n")):
        out.append(f'<text x="{x+80}" y="{82+j*16}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#444">{line.replace(chr(34), "&quot;")}</text>')
    if i < len(boxes) - 1:
        out.append(f'<line x1="{x+162}" y1="75" x2="{x+211}" y2="75" stroke="#333" stroke-width="2" marker-end="url(#a)"/>')
MEDIA.mkdir(exist_ok=True)
(MEDIA / "pipeline.svg").write_text("\n".join(out) + "\n</svg>\n")
