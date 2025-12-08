
import math
window = None
document= None
create_proxy = None

class AccelSensorName:
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"


class AccelSensor:
    def get_xyz(self):
        xyz = window.getAccelXYZ()
        x = float(xyz[0] or 0.0)
        y = float(xyz[1] or 0.0)
        z = float(xyz[2] or 0.0)
        return x, y, z

    def get_magnitude(self):
        x, y, z = self.get_xyz()
        return math.sqrt(x*x + y*y + z*z)
    
    def get_state(self, x, y, z):
        if y>7:
            return AccelSensorName.UP
        if y<-7:
            return AccelSensorName.DOWN
        if x>7:
            return AccelSensorName.LEFT
        if x<-7:
            return AccelSensorName.RIGHT


accel = AccelSensor()

def update(*args, **kwargs):
    
    x, y, z = accel.get_xyz()
    result = accel.get_state(x=x,y=y,z=z)
    m = accel.get_magnitude()
    document.getElementById("values").innerText = (
        f"x={x:.2f}, y={y:.2f}, z={z:.2f}, |a|={m:.2f}, state={result}"
    )
    window.addAccelPoint(x, y, z)

update_proxy = create_proxy(update)
window.setInterval(update_proxy, 200)