
def create_properties(id, onOff, power, energy):
    properties = {}
    if onOff:
        properties["switchA"] = {
            "type": "boolean",
            "description": "Controls the main relay of the device",
            "@type": "OnOffProperty",
            "links": [{ "href": "/things/{}/properties/switchA".format(id) }],
            "state": False
        }
    if power:
        properties["power"] = {
            "type": "number",
            "description": "Power consumption in kW",
            "links": [{
                "href": "/things/{}/properties/power".format(id)
            }],
            "state": 0
        }
    if energy:
        properties["energy"] = {
            "type": "number",
            "description": "Energy usage in kWh",
            "links": [{
                "href": "/things/{}/properties/energy".format(id)
            }],
            "state": 0
        }
    return properties

def create_types(onOff, power, energy):
    types = []
    if onOff:
        types.append("OnOffProperty")
    if power:
        types.append("PowerProperty")
    if energy:
        types.append("EnergyProperty")
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


class Thing:
    """A thing is a thing."""

    def __init__(self, thing_id, onOff, power, energy):
        self.td = create_td(thing_id, "Qube Simulator Device", onOff, power, energy)

    def get_properties(self):
        message = {
            "messageType": "getProperty",
            "thingId": self.td["id"],
            "properties": {key : value["state"] for key, value in self.td["properties"].items()}
        }
        # send this message to the client
        return message
    
    def set_property(self, propertyId, newValue):
        for key, value in self.td["properties"].items():
            if key == propertyId:
                td_copy  = self.td.copy()
                td_copy['properties'][propertyId]["state"] = newValue
                self.td = td_copy
                message = {
                    "messageType": "updatedProperty",
                    "thingId": self.td["id"],
                    "propertyId": propertyId,
                    "value": newValue
                 }
                # send this message to the client
                return message
            
        
        message = {
                    "messageType": "error",
                    "error": "Property not found"
        }
        # send this message to the client
        return message


    def get_td(self):
        return self.td

    def get_tds(self):
        message = {
            "messageType": "descriptionOfThings",
            "things": [self.td]
        }
        return message

