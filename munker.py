from PIL import Image, ImageDraw
import scipy
from scipy import special
import random
import math

# Returns the nearest multiple of `m` that is lower than `n`
def nearest_multiple(n, m):
    return ((n - m) | (m - 1)) + 1

# Returns a tuple (x, y) where (x, y) is the `nth` pair with collection size of `s`
def get_tuple(n, s, b_coef):
    # Initial value for (x, y) is (0, 1)
    x, y = 0, 1

    # Checks if `n` exceeds the binomial coefficient of `s` over 2, returns None if True
    if b_coef <= n:
        return None

    # Iterates through `n` pairs and stops at the `nth` pair
    while n > 0:
        if y == s - 1:
            x = x + 1
            y = x + 1
        else:
            y = y + 1
        n = n - 1

    return (x, y)

# TODO: implement a faster generator, avoiding collisions (pref. by spliting the image into sectors first)
# Generates `count` random coordinates on the image of size `size` with at least `c_size` pixels away from all
# generated coordinates in `circle_list` and returns the generated list
def generate_circles(count, size, c_size, b_coef):
    circle_list = []

    for i in range(count):
        while True:
            rx, ry = random.randint(0, size[0] - c_size - 1), random.randint(0, size[1] - c_size - 1)

            # Adds the generated coordinate to the `circle_list` if it is far enough from all other circles on the list
            if check_box_col(rx, ry, c_size, circle_list) == False:
                temp_len = len(circle_list)
                circle_list.append((rx, ry, temp_len % b_coef))
                
                break
    
    return circle_list

# TODO: create a faster collision function
# Unused for now
def check_col(x, y, r):
    for c in circle_list:
        dx = c[0] - x
        dy = c[1] - y

        if dx * dx + dy * dy < r * r:
            return True
        
    return False

# Temporarily using box collision instead of the circle collision function
# Checks if there is a generated circle inside the bounding box of the generated coordinate.
# Returns True if a collision is found
def check_box_col(x, y, r, circle_list):
    for c in circle_list:
        if (x + r < c[0] or x > c[0] + r) or (y + r < c[1] or y > c[1] + r):
            continue
        else:
            return True
        
    return False

# `width` parameter should not be changed. There is known bug with regards to the `width` param.
def main(colors = [(255, 255, 0),
                   (255, 0, 255),
                   (0, 255, 255),
                   (128, 128, 255)],
         c_color=(240, 180, 225),
         size=(500, 300),
         c_size=64,
         count=8,
         width=4):
    
    b_coef = 0
    circle_list = []

    # Initial check if generation of `count` circles is possible inside the image with size `size`
    # Max value for `count` should be math.floor((size[0] * size[1]) / (3 * c_size * c_size)) for this random generator implementation
    count = min(count, math.floor((size[0] * size[1]) / (3 * c_size * c_size)))

    # Init secondary params
    c_len = len(colors)
    b_coef = int(scipy.special.binom(c_len, 2))

    # Create the `Draw` object
    im = Image.new('RGB', size, (255, 255, 255))
    d = ImageDraw.Draw(im)

    # Draw lines with alternating colors from `colors` and a width of `width`
    for i in range(int(math.floor(size[1] / width))):
        d.line((0, i * width, size[0], i * width), fill=colors[i % c_len], width=width)

    # Generates a coordinate and draw `count` circles with radius `c_size` of the color `c_color`
    circle_list = generate_circles(count, size, c_size, b_coef)

    # Draws crossing lines over the circles in `circle_list`. The colors of the crossing lines depends on the 3rd element of the tuple `c` in `circle_list`
    for c in circle_list:
        d.ellipse([(c[0], c[1]), (c[0] + c_size, c[1] + c_size)], fill=c_color)
        
        for i in range(int(math.floor(c_size / width)) + 1):
            t = get_tuple(c[2], c_len, b_coef)
            f = int((c[1] + (i * width)) / width) % c_len
            ny = nearest_multiple(c[1] + i * width, width)

            if f in t:
                d.line((c[0], ny, c[0] + c_size, ny), fill=colors[f], width=width)

    im.show()

if __name__ == '__main__':
    main()
