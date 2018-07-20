from PIL import Image, ImageDraw
import scipy
from scipy import special
import random
import math

circle_list = []
b_coef = 0

# Returns the nearest multiple of `m` that is lower than `n`
def nearest_multiple(n, m):
    return ((n - m) | (m - 1)) + 1

# Returns a tuple (x, y) where (x, y) is the `nth` pair with collection size of `s`
def get_tuple(n, s):
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
# Generates a random coordinate on the image of size `size` with at least `c_size` pixels away from all
# generated coordinates in the `circle_list` and returns the generated coordinate
def gen_coord(size, c_size):
    global circle_list

    # Generates a random coordinate inside the bounding box of the image
    while True:
        rx, ry = random.randint(0, size[0] - c_size - 1), random.randint(0, size[1] - c_size - 1)

        # Adds the generated coordinate to the `circle_list` if it is far enough from all other circles on the list
        if check_box_col(rx, ry, c_size) == False:
            temp_len = len(circle_list)
            circle_list.append((rx, ry, temp_len % b_coef))
            
            return rx, ry

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
def check_box_col(x, y, r):
    for c in circle_list:
        if (x + r < c[0] or x > c[0] + r) or (y + r < c[1] or y > c[1] + r):
            continue
        else:
            return True
        
    return False

def main(colors, count, c_color, s=(500, 300), w=4, c_size=64):
    global b_coef

    # Init secondary params
    c_len = len(colors)
    b_coef = int(scipy.special.binom(c_len, 2))

    # Create the `Draw` object
    im = Image.new('RGB', s, (255, 255, 255))
    d = ImageDraw.Draw(im)

    # Draw lines with alternating colors from `colors` and a width of `w`
    for i in range(int(math.floor(s[1] / w))):
        d.line((0, i * w, s[0], i * w), fill=colors[i % c_len], width=w)

    # Generates a coordinate and draw `count` circles with radius `c_size` of the color `c_color`
    for i in range(count):
        rx, ry = gen_coord(s, c_size)
        d.ellipse([(rx, ry), (rx + c_size, ry + c_size)], fill=c_color)

    # Draws crossing lines over the circles in `circle_list`. The colors of the crossing lines depends on the 3rd element of the tuple `c` in `circle_list`
    for c in circle_list:
        for i in range(int(math.floor(c_size / w)) + 1):
            t = get_tuple(c[2], c_len)
            f = int((c[1] + (i * w)) / w) % c_len
            ny = nearest_multiple(c[1] + i * w, 4)

            if f in t:
                d.line((c[0], ny, c[0] + c_size, ny), fill=colors[f], width=w)

    im.show()

if __name__ == '__main__':
    main([(255, 255, 0),
          (255, 0, 255),
          (0, 255, 255),
          (128, 128, 255)], 15, (240, 180, 225))
