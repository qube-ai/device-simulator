import json

thing_id = input("Enter thing id: ")

onOff = input("Enter OnOffProperty (y/n): ")
if onOff == "y":
    onOff = True
else:
    onOff = False

power = input("Enter power property (y/n): ")
if power == "y":
    power = True
else:
    power = False

energy = input("Enter energy property (y/n): ")
if energy == "y":
    energy = True
else:
    energy = False


def create_properties(id, onOff, power, energy):
    properties = {}
    if onOff:
        properties["switchA"] = {
            "type": "boolean",
            "description": "Controls the main relay of the device",
            "@type": "OnOffProperty",
            "links": [{ "href": "/things/{}/properties/switchA".format(id) }]
        }
    if power:
        properties["power"] = {
            "type": "number",
            "description": "Power consumption in kW",
            "links": [{
                "href": "/things/{}/properties/power".format(id)
            }]
        }
    if energy:
        properties["energy"] = {
            "type": "number",
            "description": "Energy usage in kWh",
            "links": [{
                "href": "/things/{}/properties/energy".format(id)
            }]
        }
    return properties

def create_types(onOff, power, energy):
    types = []
    if onOff:
        types.append("OnOffProperty")
    if power:
        types.append("NumberProperty")
    if energy:
        types.append("NumberProperty")
    return types




def create_td(id, title, onOff, power, energy):
    td = {
        "id": id,
        "title": title,
        "@context": "https://webthings.io/schemas",
        "base": "https://tunnel.qube.eco/",
        "securityDefinitions": {
            "nosec_sc": {
                "scheme": "nosec"
            }
        },
        "security": "nosec_sc",
        "@type": create_types(onOff, power, energy),
        "links": [
            {   
                "rel": "properties",
                "href": "/things/{}/properties".format(id)
            },
            {
                "rel": "actions",
                "href": "/things/{}/actions".format(id)
            },
            {
                "rel": "events",
                "href": "/things/{}/events".format(id)
            },
            {   
                "rel": "alternate",
                "href": "wss://tunnel.qube.eco/things/{}".format(id)
            }

        ],
        "properties": create_properties(id, onOff, power, energy),
        "href": "/things/{}".format(id)
    }
    return td


created_td = create_td(thing_id, "Qube Simul One", onOff, power, energy)


# store created td in json file
with open("{}.json".format(thing_id), "w") as f:
    json.dump(created_td, f, indent=4)

