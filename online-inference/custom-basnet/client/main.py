import requests
import logging
import argparse
import io
from PIL import Image

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--basnet_service_host', required=True, help="The BASNet service host")
args = parser.parse_args()

# Send to BASNet service.
logging.info(' > sending to BASNet...')
source = open('images/test.png', 'rb')
files = {'data': source }
res = requests.post(args.basnet_service_host, files=files)
logging.info(res.status_code)

# Save mask locally.
logging.info(' > saving results...')
with open('images/cut_mask.png', 'wb') as f:
    f.write(res.content)
    # shutil.copyfileobj(res.raw, f)

logging.info(' > opening mask...')
mask = Image.open('images/cut_mask.png').convert("L").resize((512, 512))

# Convert string data to PIL Image.
logging.info(' > compositing final image...')
ref = Image.open(source).resize((512, 512))
empty = Image.new("RGBA", ref.size, 0)
img = Image.composite(ref, empty, mask)

# Save locally.
logging.info(' > saving final image...')
img.save('images/output.png')
