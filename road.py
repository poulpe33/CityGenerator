# To support reload properly, try to access a package var, 
# if it's there, reload everything
if "Road" in locals():
    import imp
    imp.reload(car)
    imp.reload(const)
    imp.reload(drawer)
else:
    from city_generator import car, const, drawer


import bpy
import random

class Road:
    """Class managing the roads."""

    def __init__(self, x_start, x_size, y_start, y_size, orientation,
                 city):
        """Create a new road with the given coordinates.
        Orientation is 0 (1) for a road parallel to the x-axis (y)."""
        
        # save the values
        self.x_start = x_start
        self.x_size = x_size
        self.y_start = y_start
        self.y_size = y_size
        self.orientation = orientation
        self.city = city
        
        # draw itself
        self.draw()
        
        # add cars
        if self.city.has_cars:
            self.add_cars()
    
    
    def draw(self):
        """Draw the road."""
        
        # draw the plane
        self.object = drawer.draw_relief_plane(
            self.x_start, self.x_size, self.y_start, self.y_size,
            "Road", self.city.ground.altitude_f)
        self.mesh = self.object.data

        # add the material
        self.material = bpy.data.materials.new("C_Road.000")
        self.mesh.materials.append(self.material)
        self.material.diffuse_color = (0, 0, 0)

        # add the texture
        m_tex = self.material.texture_slots.add()
        m_tex.texture_coords = 'ORCO'
        if self.orientation:
            m_tex.texture = bpy.data.textures["vert_road"].copy()
            m_tex.texture.name = "C_vert_road"
            m_tex.texture.extension = 'REPEAT'
            m_tex.texture.repeat_y = round(self.y_size)
        else:
            m_tex.texture = bpy.data.textures["hor_road"].copy()
            m_tex.texture.name = "C_hor_road"
            m_tex.texture.extension = 'REPEAT'
            m_tex.texture.repeat_x = round(self.x_size)
        
        # update
        self.mesh.update()
        
        # parent
        self.object.parent = self.city.roads_object


    def add_cars(self):
        """Add cars to the road."""
        
        min_dist = 10
        if self.orientation: # vertical
            if self.y_size < min_dist + 2:
                return
            dist = random.uniform(min_dist,
                                  min(self.y_size - 2, 3*min_dist))
            car.Car(self.x_start + 3*self.x_size/4, self.y_start + 1, 0,
                    dist, self)
            dist = random.uniform(min_dist,
                                  min(self.y_size - 2, 3*min_dist))
            car.Car(self.x_start + self.x_size/4,
                    self.y_start + self.y_size - 1, 2,
                    dist, self)
        else: # horizontal
            if self.x_size < min_dist + 2:
                return
            dist = random.uniform(min_dist,
                                  min(self.x_size - 2, 3*min_dist))
            car.Car(self.x_start + 1, self.y_start + self.y_size/4, 3,
                    dist, self)
            dist = random.uniform(min_dist,
                                  min(self.x_size - 2, 3*min_dist))
            car.Car(self.x_start + self.x_size - 1,
                    self.y_start + 3*self.y_size/4, 1,
                    dist, self)
