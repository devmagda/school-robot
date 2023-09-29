from detections import Rectangle


def calculate_average_change(rectangles1, rectangles2):
    total_change = 0
    for rect1, rect2 in zip(rectangles1, rectangles2):
        total_change += Rectangle.distance(rect1, rect2)
    return total_change / len(rectangles1)


faces = [Rectangle(50, 50, 0, 0), Rectangle(500, 500, 0, 0)]
faces2 = [Rectangle(48, 52, 0, 0), Rectangle(507, 490, 0, 0)]
faces3 = [Rectangle(48, 51, 0, 0)]
faces4 = [Rectangle(60, 60, 0, 0), Rectangle(510, 480, 0, 0)]
faces5 = [Rectangle(60, 60, 0, 0)]
faces6 = [Rectangle(60, 60, 0, 0)]
faces7 = [Rectangle(60, 60, 0, 0)]
faces8 = [Rectangle(60, 60, 0, 0)]
faces9 = [Rectangle(60, 60, 0, 0)]

# Vergleiche aufeinanderfolgende Szenen
scenes = [faces, faces2, faces3, faces4, faces5, faces6, faces7, faces8, faces9]

for i in range(len(scenes)-1):
    change = calculate_average_change(scenes[i], scenes[i+1])
    print(f'Durchschnittliche Änderung zwischen Szene {i+1} und Szene {i+2}: {change}')



from ULN2003Pi import
