size(512,512)
background(0.334)
pb = ximport("photobot")
# reload(pb)

pbh = ximport("pbhelpers")
label = pbh.label


def dogradient(s):
    sx, sy = WIDTH, HEIGHT
    inset = 10
    c = pb.canvas(sx, sy)
    #c.fill((210, 210, 10))
    c.fill((85, 85, 85))
    r1, r2 = 72, 36
    x, y = inset, inset
    w, h = sx-inset-inset, sy-inset-inset
    grad1idx = c.gradient(s, w, h, radius=r1, radius2=r2)
    mask = c.gradient(s, w, h, radius=r1, radius2=r2)
    c.layers[mask].mask()
    c.layers[grad1idx].translate(x, y)
    label(s.upper(), x, y)
    c.draw(1, 1)
    canvas._grobs.reverse()

gradients = (
    pb.SOLID,
    pb.LINEAR,
    pb.RADIAL,
    pb.DIAMOND,
    pb.SINE,
    pb.COSINE,
    pb.ROUNDRECT,
    pb.RADIALCOSINE,
    pb.QUAD)


var("Gradient", MENU, default=dogradient, value=gradients)

dogradient("solid")
