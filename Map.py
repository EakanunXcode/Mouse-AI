import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import PIL.Image
import random

# ==========================================
# ส่วนที่ 1: สร้างแผนที่เขาวงกต (Maze Generation)
# ==========================================
def generate_maze(width=30, height=30):
    # สร้าง Grid เริ่มต้นที่เป็นกำแพงทั้งหมด (1 = กำแพง, 0 = ทางเดิน)
    maze = np.ones((height * 2 + 1, width * 2 + 1))
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    def carve_passages_from(cx, cy):
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny * 2 + 1, nx * 2 + 1] == 1:
                maze[cy * 2 + 1 + dy, cx * 2 + 1 + dx] = 0
                maze[ny * 2 + 1, nx * 2 + 1] = 0
                carve_passages_from(nx, ny)

    maze[1, 1] = 0
    carve_passages_from(0, 0)
    return maze

# สร้างตัวแปร maze_grid ขึ้นมาเก็บแผนที่ที่ถูกสุ่ม
maze_grid = generate_maze(30, 30)

# กำหนดจุด Start และ End
start_pos = (1, 1)
end_pos = (59, 59)

# ==========================================
# ส่วนที่ 2: การแสดงผลกราฟิกและวางหนู (Visualization)
# ==========================================
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(maze_grid, cmap='bone')

# ฟังก์ชันเสริมสำหรับเอารูปภาพ PNG มาวางบนพิกัด
def add_custom_sprite(ax, img_path, xy, zoom=0.1):
    try:
        img = PIL.Image.open(img_path)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, xy, frameon=False)
        ax.add_artist(ab)
    except FileNotFoundError:
        # ถ้าหาไฟล์รูปหนูไม่เจอ จะแสดงผลเป็นวงกลมสีฟ้าแทนอัตโนมัติ
        ax.scatter(xy[0], xy[1], color='dodgerblue', s=200, label='Blue Mouse (Missing File)', zorder=5)

# สลับพิกัดให้เป็น (X, Y) สำหรับ Matplotlib
mouse_xy = (start_pos[1], start_pos[0]) 
cheese_xy = (end_pos[1], end_pos[0])

# วางรูปหนูสีฟ้า (อย่าลืมเอาไฟล์ blue_mouse.png ไว้โฟลเดอร์เดียวกับ Map.py)
add_custom_sprite(ax, 'blue_mouse.png', mouse_xy, zoom=0.08)

# วางชีส
ax.scatter(cheese_xy[0], cheese_xy[1], color='gold', s=150, label='Cheese', zorder=5)

plt.title("AI for Robotics: Cute Blue Mouse Maze", fontsize=16)
plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
plt.axis('off')
plt.tight_layout()

# แสดงผลหน้าจอ
plt.show()