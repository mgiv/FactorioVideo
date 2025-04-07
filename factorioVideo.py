#!/usr/bin/env python
import base64
import zlib
import json
from signals import signals
import image


class Image:
    def __init__(self, image_in):
        self.hex_image = image_in
        self.int_image = [[int(y, 16) for y in x] for x in image_in]

    def __str__(self):
        return str(self.int_image)


class FactorioBlueprint:
    @staticmethod
    def decode_blueprint():
        blueprint_cut = blueprint_encoded[1:]
        decoded = base64.b64decode(blueprint_cut)
        inflated = zlib.decompress(decoded)
        return inflated

    def jsonify(self):
        return json.loads(self.blueprint)

    def __init__(self, blueprint_in):
        self.blueprint_encoded = blueprint_in
        self.blueprint_deflated = self.decode_blueprint()
        self.blueprint = self.blueprint_deflated.decode('ascii')
        self.json = self.jsonify()

blueprint_encoded = open("signals.factorioblueprint", "r").read()
blueprint = FactorioBlueprint(blueprint_encoded)
open("out.json", "w").write(json.dumps(blueprint.json, indent=4))

images = image.get_images()

filters = blueprint.json['blueprint']['entities'][0]['control_behavior']['sections']['sections'][0]['filters']

for filter in filters:
    idx = filter['index']
    filter['count'] = images[0][0][idx - 1]


blueprint_compressed = zlib.compress(json.dumps(blueprint.json, indent=4).encode('utf-8'))
print("0" + base64.b64encode(blueprint_compressed).decode('utf-8'))