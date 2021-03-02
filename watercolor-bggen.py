import cairo, sys, argparse, copy, math, random
import numpy as np

float_gen = lambda a, b: random.uniform(a, b)

colors = []
for i in range(15):
    #colors.append((float_gen(.4, .75), float_gen(.4, .75), float_gen(.4, .75)))
    colors.append((float_gen(.5, .95), float_gen(.0, .6), float_gen(.5, .95)))

def gauss_cut(mu, sigma):
    """
        cut gauss distribution into [0,1]
    """
    r = random.gauss(mu, sigma)
    while r < 0 or r > 1:
        r = random.gauss(mu, sigma)
    return r

def multi_variate_gaussian_cut(mean,cov):
    sample = np.random.multivariate_normal(mean, cov)
    for i in range(len(sample)):
        if sample[i]<0:
            sample[i]=0
        elif sample[i]>1:
            sample[i]=1
    return sample

def octagon(x_orig, y_orig, side):
    x = x_orig
    y = y_orig
    d = side / math.sqrt(2)

    oct = []

    oct.append((x, y))

    x += side
    oct.append((x, y))

    x += d
    y += d
    oct.append((x, y))

    y += side
    oct.append((x, y))

    x -= d
    y += d
    oct.append((x, y))

    x -= side
    oct.append((x, y))

    x -= d
    y -= d
    oct.append((x, y))

    y -= side
    oct.append((x, y))

    x += d
    y -= d
    oct.append((x, y))

    return oct

def deform(shape, iterations, variance):
    for i in range(iterations):
        for j in range(len(shape)-1, 0, -1):
            midpoint = ((shape[j-1][0] + shape[j][0])/2 + float_gen(-variance, variance), (shape[j-1][1] + shape[j][1])/2 + float_gen(-variance, variance))
            shape.insert(j, midpoint)
    return shape


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", default=1200, type=int)
    parser.add_argument("--height", default=600, type=int)
    parser.add_argument("-i", "--initial", default=120, type=int)
    parser.add_argument("-d", "--deviation", default=50, type=int)
    parser.add_argument("-bd", "--basedeforms", default=1, type=int)
    parser.add_argument("-fd", "--finaldeforms", default=3, type=int)
    parser.add_argument("-mins", "--minshapes", default=20, type=int)
    parser.add_argument("-maxs", "--maxshapes", default=25, type=int)
    parser.add_argument("-sa", "--shapealpha", default=.017, type=float)
    args = parser.parse_args()

    width, height = args.width, args.height
    initial = args.initial
    deviation = args.deviation

    basedeforms = args.basedeforms
    finaldeforms = args.finaldeforms

    minshapes = args.minshapes
    maxshapes = args.maxshapes

    shapealpha = args. shapealpha

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    #cr.set_source_rgb(.9, .9, .9)
    cr.set_source_rgb(.1, .1, .2)
    cr.rectangle(0, 0, width, height)
    cr.fill()

    cr.set_line_width(1)
    mean = [0.7,0.2,0.7]
    sigma_r = 0.3
    sigma_g = 0.3
    sigma_b = 0.3
    sigma_rg = 0.1
    sigma_rb = 0.1
    sigma_bg = 0.1
    cov = [[sigma_r,sigma_rg,sigma_rb],[sigma_rg,sigma_g,sigma_bg],[sigma_rb,sigma_bg,sigma_b]]
    for p in range(-int(height*.2), int(height*1.2), 20):
        #couleur = [float_gen(.5, .95), float_gen(.3, .6), float_gen(.5, .95)]
        #couleur = [gauss_cut(0.7,0.3), gauss_cut(0.4,0.3),gauss_cut(0.7,0.3)]
        couleur = multi_variate_gaussian_cut(mean,cov)
        cr.set_source_rgba(couleur[0], couleur[1], couleur[2], float_gen(shapealpha*0.8, shapealpha*1.2))

        #cr.set_source_rgba(random.choice(colors)[0], random.choice(colors)[1], random.choice(colors)[2], shapealpha)

        shape = octagon(random.randint(-100, width+100), p, random.randint(100, 300))
        baseshape = deform(shape, basedeforms, initial)

        for j in range(random.randint(minshapes, maxshapes)):
            tempshape = copy.deepcopy(baseshape)
            layer = deform(tempshape, finaldeforms, deviation)

            for i in range(len(layer)):
                cr.line_to(layer[i][0], layer[i][1])
            cr.fill()

    ims.write_to_png('Examples/watercolor' + str(int(random.randint(0, 500))) + '.png')

if __name__ == "__main__":
    main()