# Molecular geometry and symmetry numerical kernel in Julia.

function distance(a, b)
    return sqrt(sum((a .- b).^2))
end

function angle_degrees(a, b, c)
    u = a .- b
    v = c .- b
    cos_theta = dot(u, v) / (sqrt(dot(u, u)) * sqrt(dot(v, v)))
    return acos(clamp(cos_theta, -1.0, 1.0)) * 180.0 / pi
end

function rotation_matrix_z(theta_degrees)
    theta = theta_degrees * pi / 180.0
    return [
        cos(theta) -sin(theta) 0.0;
        sin(theta) cos(theta) 0.0;
        0.0 0.0 1.0
    ]
end

oxygen = [0.0, 0.0, 0.0]
h1 = [0.958, 0.0, 0.0]
h2 = [-0.239, 0.927, 0.0]

println("OH distance angstrom=", round(distance(oxygen, h1), digits=6))
println("HOH angle degrees=", round(angle_degrees(h1, oxygen, h2), digits=3))
println("Rz 120 first row=", rotation_matrix_z(120.0)[1, :])
