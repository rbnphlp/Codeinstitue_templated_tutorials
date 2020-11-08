import tensorflow as tf


import IPython.display as display

import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np
import PIL.Image
import time
import functools


new_width  = 380
new_height = 512

def get_concat_v_resize(im1, im2, resample=PIL.Image.BICUBIC, resize_big_image=True):
    if im1.width == im2.width:
        _im1 = im1
        _im2 = im2
    elif (((im1.width > im2.width) and resize_big_image) or
          ((im1.width < im2.width) and not resize_big_image)):
        _im1 = im1.resize((im2.width, int(im1.height * im2.width / im1.width)), resample=resample)
        _im2 = im2
    else:
        _im1 = im1
        _im2 = im2.resize((im1.width, int(im2.height * im1.width / im2.width)), resample=resample)
    dst = PIL.Image.new('RGB', (_im1.width, _im1.height + _im2.height))
    dst.paste(_im1, (0, 0))
    dst.paste(_im2, (0, _im1.height))
    return dst


def tensor_to_image(tensor):
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return PIL.Image.fromarray(tensor)


def load_img(path_to_img):
  max_dim = 512
  img = tf.io.read_file(path_to_img)
  img = tf.image.decode_image(img, channels=3)
  img = tf.image.convert_image_dtype(img, tf.float32)

  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim / long_dim

  new_shape = tf.cast(shape * scale, tf.int32)

  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  return img


def imshow(image, title=None):
  if len(image.shape) > 3:
    image = tf.squeeze(image, axis=0)

  plt.imshow(image)
  if title:
    plt.title(title)

  

" loop through upload pics  and style pics  and generate painitns "


mypath='upload_pics'
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for files in onlyfiles:
    
    file_=mypath+"/"+files
    content_path = file_
    style_path = "style_pics/red_style.jpeg"



    content_image = load_img(content_path)
    style_image = load_img(style_path)

    "load images "
    content_image_pil = PIL.Image.open(content_path)
    style_image_pil = PIL.Image.open(style_path)
    "Combine the style and upload Pic togetger "
    combined_image=get_concat_v_resize(content_image_pil, style_image_pil, resize_big_image=False)
    combined_image=combined_image.resize((new_width, new_height), PIL.Image.ANTIALIAS)
    combined_image.save('combined'+"/"+'red_style'+files)
    



    import tensorflow_hub as hub
    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
    l=tensor_to_image(stylized_image)

    # Resize image
   
    l= l.resize((new_width, new_height), PIL.Image.ANTIALIAS)

    # creating a image object (main image)  
    l.save("paintings"+"/"+"painiting_human_style"+files)  
    