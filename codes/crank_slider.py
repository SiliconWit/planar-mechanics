import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Given dimensions in mm
OA_mm = 150
AB_mm = 500
OB_mm = 450

# Convert dimensions to meters
OA_m = OA_mm * 1e-3
AB_m = AB_mm * 1e-3
OB_m = OB_mm * 1e-3

# Given angular speed in RPM
omega_OA_rpm = 120
# Convert angular speed to rad/s
omega_OA_rad_s = omega_OA_rpm * (2 * np.pi / 60)

# Given angular acceleration in rad/s²
alpha_OA_rad_s2 = 30

def calculate_positions(theta_OA_rad):
    """Calculate positions of points A and B for given angle"""
    # Position of A (this will create a perfect circle)
    x_A = OA_m * np.cos(theta_OA_rad)
    y_A = OA_m * np.sin(theta_OA_rad)
    
    # Position of B (moves horizontally, y_B = 0)
    # Using constraint that distance AB = AB_m
    x_B = x_A + np.sqrt(AB_m**2 - y_A**2)
    y_B = 0
    
    return x_A, y_A, x_B, y_B

def calculate_kinematics(theta_OA_rad, omega_OA_rad_s, alpha_OA_rad_s2):
    """Calculate velocities and accelerations"""
    x_A, y_A, x_B, y_B = calculate_positions(theta_OA_rad)
    
    # Angular velocity of OA
    omega_OA = np.array([0, 0, omega_OA_rad_s])
    
    # Velocity of A
    v_A = np.cross(omega_OA, np.array([x_A, y_A, 0]))
    
    # Velocity of B
    v_B = omega_OA_rad_s * OA_m * np.sin(theta_OA_rad)
    
    # Relative velocity (v_AB)
    v_AB = v_B - v_A[0]
    
    # Angular velocity of AB
    omega_AB = v_AB / AB_m
    
    # Angular acceleration of OA
    alpha_OA = np.array([0, 0, alpha_OA_rad_s2])
    
    # Normal acceleration of A
    a_A_n = -omega_OA_rad_s**2 * np.array([x_A, y_A, 0])
    
    # Tangential acceleration of A
    a_A_t = np.cross(alpha_OA, np.array([x_A, y_A, 0]))
    
    # Total acceleration of A
    a_A = a_A_n + a_A_t
    
    # Acceleration of B
    a_B = alpha_OA_rad_s2 * OA_m * np.sin(theta_OA_rad) - omega_OA_rad_s**2 * OA_m * np.cos(theta_OA_rad)
    
    return v_A, v_B, omega_AB, a_A, a_B

# Set up the figure with subplots
fig = plt.figure(figsize=(16, 12))

# Create subplot layout
ax1 = plt.subplot(2, 3, (1, 4))  # Main animation (spans 2 rows, left column)
ax2 = plt.subplot(2, 3, 2)       # Angular position plot
ax3 = plt.subplot(2, 3, 3)       # Velocity plot
ax4 = plt.subplot(2, 3, 5)       # Acceleration plot
ax5 = plt.subplot(2, 3, 6)       # Angular velocity plot

# Animation parameters
dt = 0.08  # Slower time step for better visualization
t_max = 4 * np.pi / omega_OA_rad_s  # Two complete rotations
time_steps = np.arange(0, t_max, dt)

# Main animation subplot
ax1.set_xlim(-0.25, 0.75)
ax1.set_ylim(-0.25, 0.25)
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)
ax1.set_xlabel('X (m)')
ax1.set_ylabel('Y (m)')
ax1.set_title('Four-Bar Linkage Mechanism Animation', fontsize=14, fontweight='bold')

# Draw circular reference for point A
circle_A = plt.Circle((0, 0), OA_m, fill=False, linestyle=':', color='red', alpha=0.5, linewidth=1)
ax1.add_patch(circle_A)

# Initialize plot elements
line_OA, = ax1.plot([], [], 'ro-', linewidth=4, markersize=10, label='Link OA', markerfacecolor='red')
line_AB, = ax1.plot([], [], 'bo-', linewidth=4, markersize=10, label='Link AB', markerfacecolor='blue')
slider_track, = ax1.plot([], [], 'k-', linewidth=3, alpha=0.7, label='Slider track')
trail_A, = ax1.plot([], [], 'r-', alpha=0.8, linewidth=2, label='Trail A (circular)')
trail_B, = ax1.plot([], [], 'b-', alpha=0.8, linewidth=2, label='Trail B')

# Velocity vectors
vel_A_arrow = ax1.annotate('', xy=(0, 0), xytext=(0, 0), 
                          arrowprops=dict(arrowstyle='->', color='red', lw=3))
vel_B_arrow = ax1.annotate('', xy=(0, 0), xytext=(0, 0), 
                          arrowprops=dict(arrowstyle='->', color='blue', lw=3))

# Text displays
info_text = ax1.text(0.02, 0.98, '', transform=ax1.transAxes, fontsize=11,
                     verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))

ax1.legend(loc='upper right', fontsize=10)

# Setup other plots
plots_config = [
    (ax2, 'Angular Position (rad)', 'θ_OA vs Time', 'green'),
    (ax3, 'Velocity (m/s)', 'Velocities vs Time', None),
    (ax4, 'Acceleration (m/s²)', 'Accelerations vs Time', None),
    (ax5, 'Angular Velocity (rad/s)', 'Angular Velocities vs Time', None)
]

for ax, ylabel, title, color in plots_config:
    ax.set_xlabel('Time (s)')
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=11)
    ax.grid(True, alpha=0.3)

# Initialize plot lines
angle_line, = ax2.plot([], [], 'g-', linewidth=2, label='θ_OA')
ax2.legend()

vel_A_line, = ax3.plot([], [], 'r-', linewidth=2, label='|v_A|')
vel_B_line, = ax3.plot([], [], 'b-', linewidth=2, label='v_B')
ax3.legend()

acc_A_line, = ax4.plot([], [], 'r-', linewidth=2, label='|a_A|')
acc_B_line, = ax4.plot([], [], 'b-', linewidth=2, label='a_B')
ax4.legend()

omega_OA_line, = ax5.plot([], [], 'g-', linewidth=2, label='ω_OA')
omega_AB_line, = ax5.plot([], [], 'm-', linewidth=2, label='ω_AB')
ax5.legend()

# Storage for data
trail_A_x, trail_B_x = [], []
trail_A_y, trail_B_y = [], []
time_data = []
angle_data, vel_A_data, vel_B_data = [], [], []
acc_A_data, acc_B_data = [], []
omega_OA_data, omega_AB_data = [], []

def animate(frame):
    t = time_steps[frame]
    
    # Calculate current angle (with angular acceleration)
    theta_OA_rad = omega_OA_rad_s * t + 0.5 * alpha_OA_rad_s2 * t**2
    current_omega = omega_OA_rad_s + alpha_OA_rad_s2 * t
    
    # Calculate positions
    x_A, y_A, x_B, y_B = calculate_positions(theta_OA_rad)
    
    # Calculate kinematics
    v_A, v_B, omega_AB, a_A, a_B = calculate_kinematics(theta_OA_rad, current_omega, alpha_OA_rad_s2)
    
    # Update mechanism links
    line_OA.set_data([0, x_A], [0, y_A])
    line_AB.set_data([x_A, x_B], [y_A, y_B])
    
    # Update slider track
    slider_track.set_data([x_B-0.05, x_B+0.05], [0, 0])
    
    # Update trails - ensuring A trail is perfectly circular
    trail_A_x.append(x_A)
    trail_A_y.append(y_A)
    trail_B_x.append(x_B)
    trail_B_y.append(y_B)
    
    # Limit trail length for performance
    trail_length = 300
    if len(trail_A_x) > trail_length:
        trail_A_x.pop(0)
        trail_A_y.pop(0)
        trail_B_x.pop(0)
        trail_B_y.pop(0)
    
    trail_A.set_data(trail_A_x, trail_A_y)
    trail_B.set_data(trail_B_x, trail_B_y)
    
    # Update velocity vectors (scaled for visibility)
    vel_scale = 0.08
    vel_A_arrow.set_position((x_A, y_A))
    vel_A_arrow.xy = (x_A + v_A[0]*vel_scale, y_A + v_A[1]*vel_scale)
    
    vel_B_arrow.set_position((x_B, y_B))
    vel_B_arrow.xy = (x_B + v_B*vel_scale, y_B)
    
    # Update information text
    info_str = f'Time: {t:.2f} s\n'
    info_str += f'θ_OA: {np.degrees(theta_OA_rad):.1f}°\n'
    info_str += f'ω_OA: {current_omega:.2f} rad/s\n'
    info_str += f'ω_AB: {omega_AB:.2f} rad/s\n'
    info_str += f'|v_A|: {np.linalg.norm(v_A[:2]):.3f} m/s\n'
    info_str += f'v_B: {v_B:.3f} m/s\n'
    info_str += f'|a_A|: {np.linalg.norm(a_A[:2]):.3f} m/s²\n'
    info_str += f'a_B: {a_B:.3f} m/s²'
    info_text.set_text(info_str)
    
    # Update data arrays
    time_data.append(t)
    angle_data.append(theta_OA_rad)
    vel_A_data.append(np.linalg.norm(v_A[:2]))
    vel_B_data.append(abs(v_B))
    acc_A_data.append(np.linalg.norm(a_A[:2]))
    acc_B_data.append(abs(a_B))
    omega_OA_data.append(current_omega)
    omega_AB_data.append(omega_AB)
    
    # Limit data length
    data_length = 400
    if len(time_data) > data_length:
        time_data.pop(0)
        angle_data.pop(0)
        vel_A_data.pop(0)
        vel_B_data.pop(0)
        acc_A_data.pop(0)
        acc_B_data.pop(0)
        omega_OA_data.pop(0)
        omega_AB_data.pop(0)
    
    # Update all plots
    angle_line.set_data(time_data, angle_data)
    vel_A_line.set_data(time_data, vel_A_data)
    vel_B_line.set_data(time_data, vel_B_data)
    acc_A_line.set_data(time_data, acc_A_data)
    acc_B_line.set_data(time_data, acc_B_data)
    omega_OA_line.set_data(time_data, omega_OA_data)
    omega_AB_line.set_data(time_data, omega_AB_data)
    
    # Auto-scale all plots
    for ax in [ax2, ax3, ax4, ax5]:
        ax.relim()
        ax.autoscale_view()
    
    return (line_OA, line_AB, slider_track, trail_A, trail_B, vel_A_arrow, vel_B_arrow, 
            info_text, angle_line, vel_A_line, vel_B_line, acc_A_line, acc_B_line, 
            omega_OA_line, omega_AB_line)

# Create animation with slower speed
anim = animation.FuncAnimation(fig, animate, frames=len(time_steps), 
                             interval=80, blit=False, repeat=True)

plt.tight_layout()

# Print initial conditions
print("Enhanced Four-Bar Linkage Analysis:")
print(f"OA: {OA_m:.3f} m, AB: {AB_m:.3f} m, OB: {OB_m:.3f} m")
print(f"Initial angular speed (ω_OA): {omega_OA_rad_s:.4f} rad/s")
print(f"Angular acceleration (α_OA): {alpha_OA_rad_s2:.4f} rad/s²")
print("\nFeatures:")
print("- Perfect circular trail for point A")
print("- Live velocity and acceleration plots")
print("- Angular velocity tracking")
print("- Slower animation for better observation")

# Show the animation
plt.show()

# Optional: Save animation as gif (uncomment the line below)
# anim.save('enhanced_linkage_mechanism.gif', writer='pillow', fps=12)
