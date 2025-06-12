from PIL import Image, ImageEnhance

def overlay_mask(image_path, mask_path):

  # Load the image and mask
  image = Image.open(image_path)
  mask = Image.open(mask_path).convert("RGBA")

  # Overlay the mask on the image
  image.paste(mask, (0, 0), mask)

  # Increase brightness by 70%
  enhancer = ImageEnhance.Brightness(image)
  image = enhancer.enhance(1.7) 
  image.save('./image_with_mask/display.jpg')
