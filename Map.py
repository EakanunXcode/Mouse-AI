import numpy as np
import matplotlib.pyplot as plt
import random

def generate_maze(width=30, height=30):
    # สร้าง Grid เริ่มต้นที่เป็นกำแพงทั้งหมด (1 = กำแพง, 0 = ทางเดิน)
    # ขนาดจริงจะคูณ 2 + 1 เพื่อให้มีพื้นที่สำหรับสร้างกำแพงกั้นระหว่างช่อง
    maze = np.ones((height * 2 + 1, width * 2 + 1))
    
    # กำหนดทิศทางการเดิน (ขึ้น, ลง, ซ้าย, ขวา)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    def carve_passages_from(cx, cy):
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            # ตรวจสอบว่าช่องถัดไปอยู่ในขอบเขตและยังเป็นกำแพงอยู่หรือไม่
            if 0 <= nx < width and 0 <= ny < height and maze[ny * 2 + 1, nx * 2 + 1] == 1:
                # ทุบกำแพงระหว่างช่องปัจจุบันกับช่องถัดไป
                maze[cy * 2 + 1 + dy, cx * 2 + 1 + dx] = 0
                # ทำช่องถัดไปให้เป็นทางเดิน
                maze[ny * 2 + 1, nx * 2 + 1] = 0
                carve_passages_from(nx, ny)

    # เริ่มเจาะเขาวงกตจากจุด (0,0)
    maze[1, 1] = 0
    carve_passages_from(0, 0)
    
    return maze

# 1. สร้างเขาวงกตขนาด 30x30
maze_grid = generate_maze(30, 30)

# 2. กำหนดจุดเริ่มต้น (หนู) และจุดหมาย (ชีส)
# หนู (สีเขียว) เริ่มที่มุมซ้ายบน, ชีส (สีเหลือง/ทอง) อยู่ที่มุมขวาล่าง
start_pos = (1, 1)
end_pos = (59, 59) # 30*2 - 1

# 3. ตั้งค่าการแสดงผลด้วย Matplotlib
plt.figure(figsize=(10, 10))
plt.imshow(maze_grid, cmap='bone') # ใช้สีขาวดำสำหรับทางเดินและกำแพง

# วางตำแหน่งหนู (Start)
plt.scatter(start_pos[1], start_pos[0], color='green', s=100, label='Start (Mouse)', zorder=5)

# วางตำแหน่งชีส (End)
plt.scatter(end_pos[1], end_pos[0], color='gold', s=100, label='End (Cheese)', zorder=5)

plt.title("AI for Robotics: 30x30 Random Maze", fontsize=16)
plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
plt.axis('off') # ปิดตัวเลขแกน X, Y เพื่อความสวยงาม

# แสดงผล (แคปจอนี้ส่งได้เลย)
plt.tight_layout()
plt.show()