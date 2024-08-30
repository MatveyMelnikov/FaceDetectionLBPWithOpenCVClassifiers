from PIL import Image, ImageEnhance
import os


def grey_scale_and_size(path):
    ind = 0

    for _file in os.listdir(path):
        if _file.endswith('.jpg'):
            img = Image.open((os.path.join(path, _file))).convert('L')
            img = img.resize((512, 512), Image.Resampling.LANCZOS)
            img = ImageEnhance.Contrast(img).enhance(2)
            img.save(path + '/output/' + ind.__str__() + '.jpg')
            img.close()
            ind += 1


grey_scale_and_size('dataset_faces')
