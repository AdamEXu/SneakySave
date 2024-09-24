from PIL import ImageTk, Image, ImageDraw, ImageFont
import os
import json as json
import requests

def hex_to_rgb(hex):
  return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def generate_coverslide(uid):
  path = f"static/user_data/{uid}/"
  os.makedirs(path, exist_ok=True)
  # get the save data
  with open(f"saves/{uid}/essentials/save0.json", "r") as f:
    save0 = json.load(f)
  with open(f"saves/{uid}/essentials/save1.json", "r") as f:
    save1 = json.load(f)
  with open(f"saves/{uid}/essentials/save2.json", "r") as f:
    save2 = json.load(f)
  
  # generate the coverslide from user_gentemplate.png and add text onto it then save to path as generated_coverslide.png
  total_coins = save0["coins"] + save1["coins"] + save2["coins"]
  total_days = save0["days"] + save1["days"] + save2["days"]
  # get user data
  with open("users.json", "r") as f:
    users = json.load(f)
    user = users[uid]
  username = user["username"]
  profile_pic_url = user["avatar"]
  # generate the image with pillow
  image = Image.open("user_gentemplate.png").convert("RGBA")
  # draw the profile picture near the center
  # note that profile picture is a url
  if profile_pic_url == "/static/resources/images/temp_profile.jpg":
    profile_pic = Image.open(profile_pic_url).convert("RGBA")
  else:
    profile_pic = Image.open(requests.get(profile_pic_url, stream=True).raw).convert("RGBA")
  profile_pic = profile_pic.resize((160, 160))

  # Create a circular mask
  mask = Image.new('L', (160, 160), 0)
  draw_mask = ImageDraw.Draw(mask)
  draw_mask.ellipse((0, 0, 160, 160), fill=255)

  # Apply the mask to the profile picture
  profile_pic.putalpha(mask)

  # Now paste the profile picture onto the image with mask
  image.paste(profile_pic, (600, 360), profile_pic)

  # now draw the username to the right of the profile picture
  draw = ImageDraw.Draw(image)
  draw.text((800, 375), username, fill=hex_to_rgb("2f5327"), font=ImageFont.truetype("Jost-SemiBold.ttf", size=100))
  font = ImageFont.truetype("Jost-Light.ttf", size=70)

  # Draw coins
  text = f"{total_coins:,d} total coins"
  text_width = font.getlength(text)

  # Calculate the x-coordinate for centering (assuming 1920 is the image width)
  x = (image.width - text_width) // 2

  # Draw the centered text
  draw.text((x, 550), text, fill=hex_to_rgb("71b150"), font=font)

  # Draw days
  text = f"{total_days:,d} total days"
  text_width = font.getlength(text)

  # Calculate the x-coordinate for centering (assuming 1920 is the image width)
  x = (image.width - text_width) // 2
  draw.text((x, 650), text, fill=hex_to_rgb("71b150"), font=font)
  
  image.save(f"{path}generated_coverslide.png")

if __name__ == "__main__":
  generate_coverslide("773996537414942763")