import os 
import json
from image_utils import generate_coverslide

uid = "773996537414942763"

def check_save_file_valid(save):
  save = save.split('\n')
  # make sure that ***********CLOUDPROFILE0, ***********CLOUDPROFILE1, etc exist
  for i in range(3):
    if f"**********CLOUDPROFILE{str(i+1)}" not in save:
      return False
  return True

def create_save_index(uid):
  path = f"saves/{uid}/"
  os.makedirs(path, exist_ok=True)
  return path

def get_save_data(uid, path, index):
  path = f"saves/{uid}/{path}"
  # index is in the format of something.otherthing.yetanotherthing
  # the file at path will contain what is a json file, so we can use the json module to parse it.
  # we want the equivalent of json.loads(open(path).read())[something][otherthing][yetanotherthing]
  with open(path, "r") as f:
    data = json.loads(f.read())
    for i in index.split("."):
      data = data[i]
    return data

def update_save_index(uid, save):
  if not check_save_file_valid(save):
    return False

  path = create_save_index(uid)
  # save is a string containing the save data.
  # we want to keep only the cloud save data.
  # delete everything before **********CLOUDPROFILE0
  # first clean the data
  save = save.split("*"*10+"CLOUDPROFILE0")[1]
  # now, there are 3 saves, CLOUDPROFILE1, CLOUDPROFILE2, CLOUDPROFILE3
  # we want to create a list of saves
  saves = []
  saves.append(save.split("*"*10+"CLOUDPROFILE1")[0])
  save = save.split("*"*10+"CLOUDPROFILE1")[1]
  saves.append(save.split("*"*10+"CLOUDPROFILE2")[0])
  save = save.split("*"*10+"CLOUDPROFILE2")[1]
  saves.append(save.split("*"*10+"CLOUDPROFILE3")[0])
  saves.append(save)

  # save 1
  os.makedirs(f"saves/{uid}/save0", exist_ok=True)
  os.makedirs(f"saves/{uid}/save0/map", exist_ok=True)
  save = saves[0]
  save = save.split("--------default/")[1:]
  for s in save:
    # remove bytes by splitting by new lines and taking [1]
    path = s.split(" ")[0]
    data = s.split(" ")[1:]
    data = s.split('\n')[1:]
    with open(f"saves/{uid}/save0/{path}", "w") as f:
      f.write("".join(data))
  
  # save 2
  os.makedirs(f"saves/{uid}/save1", exist_ok=True)
  os.makedirs(f"saves/{uid}/save1/map", exist_ok=True)
  save = saves[1]
  save = save.split("--------default2/")[1:]
  for s in save:
    path = s.split(" ")[0]
    data = s.split(" ")[1:]
    data = s.split('\n')[1:]
    with open(f"saves/{uid}/save1/{path}", "w") as f:
      f.write("".join(data))

  # save 3
  os.makedirs(f"saves/{uid}/save2", exist_ok=True)
  os.makedirs(f"saves/{uid}/save2/map", exist_ok=True)
  save = saves[2]
  save = save.split("--------default3/")[1:]
  for s in save:
    path = s.split(" ")[0]
    data = s.split(" ")[1:]
    data = s.split('\n')[1:]
    with open(f"saves/{uid}/save2/{path}", "w") as f:
      f.write("".join(data))
  
  # now create an essentials folder, which will contains jsons containing the most important data
  os.makedirs(f"saves/{uid}/essentials", exist_ok=True)
  # save0.json, save1.json, save2.json

  for i in range(3):
    # open equipment.stuff and get the vehicles
    vehicles = {}
    vehicles_raw = get_save_data(uid, f"save{str(i)}/equipment.stuff", "vehicles")

    for vehicle in vehicles_raw:
      if "color" not in vehicle:
        vehicle["color"] = "default"
      if "m" not in vehicle:
        vehicle["m"] = []
      if "lvl" not in vehicle:
        vehicle["lvl"] = 1
      vehicles[vehicle["id"]] = {
        "lvl": vehicle["lvl"],
        "color": vehicle["color"],
        "mods": vehicle["m"]
      }

    # find number of map pieces by searching for map_seg# in inventory.stuff where # is a number
    items = get_save_data(uid, f"save{str(i)}/inventory.stuff", "items")

    map_pieces = 0
    for item in items:
      if "mapseg_" in item["type"]:
        map_pieces += 1

    essentials = {
      "coins": get_save_data(uid, f"save{str(i)}/sasquatch.stuff", "coins"),
      "bankcoin": get_save_data(uid, f"save{str(i)}/sasquatch.stuff", "bankcoin"),
      "lumber": get_save_data(uid, f"save{str(i)}/sasquatch.stuff", "lumber"),
      "days": get_save_data(uid, f"save{str(i)}/sasquatch.stuff", "day"),
      "last_updated": get_save_data(uid, f"save{str(i)}/user.stuff", "st"),
      "vehicles": vehicles,
      "map_pieces": map_pieces,
    }

    with open(f"saves/{uid}/essentials/save{str(i)}.json", "w") as f:
      f.write(json.dumps(essentials, indent=2))
  if uid != "temp":
    generate_coverslide(uid)
  else:
    # remove the temp save
    os.rmdir(f"saves/{uid}")

  return True

# with open("test.txt", "r") as f:
#   save = f.read()
#   update_save_index(uid, save)