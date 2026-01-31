#!/usr/bin/env bash
set -euo pipefail
# Show the phone access URL and QR code for the Sejrliste web app
LOCAL_IP=$(hostname -I | awk '{print $1}')
URL="http://${LOCAL_IP}:8501"

echo ""
echo "================================================"
echo "  SEJRLISTE — PHONE ACCESS"
echo "================================================"
echo ""
echo "  Open this URL on your phone:"
echo ""
echo "    $URL"
echo ""

# Try to generate QR code using the project venv
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON="${SCRIPT_DIR}/venv/bin/python3"

if [ ! -x "$PYTHON" ]; then
    PYTHON="python3"
fi

"$PYTHON" -c "
import sys
try:
    import qrcode
    qr = qrcode.QRCode(version=1, box_size=1, border=1)
    qr.add_data('$URL')
    qr.make(fit=True)
    matrix = qr.get_matrix()
    for row in matrix:
        line = '  '
        for cell in row:
            line += chr(9608)*2 if cell else '  '
        print(line)
except ImportError:
    print('  (Install qrcode: pip install qrcode[pil])')
" 2>/dev/null

echo ""
echo "  (Phone must be on same WiFi / hotspot)"
echo "================================================"
echo ""
