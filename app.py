from flask import Flask, render_template, request, send_file
from io import BytesIO

app = Flask(__name__)

def generate_bash_script(images, names, host_ports, container_ports, volumes, env_lists):
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "# Update and install prerequisites",
        "sudo apt-get update",
        "sudo apt-get install -y ca-certificates curl gnupg lsb-release",
        "",
        "# Add Docker’s official GPG key and repository",
        "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg",
        'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] '
        'https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | '
        'sudo tee /etc/apt/sources.list.d/docker.list > /dev/null',
        "",
        "# Install Docker Engine",
        "sudo apt-get update",
        "sudo apt-get install -y docker-ce docker-ce-cli containerd.io",
        "",
        "# Add current user to docker group",
        "sudo usermod -aG docker $USER",
        "",
        "# Enable Docker service",
        "sudo systemctl enable docker",
        "sudo systemctl start docker",
        ""
    ]

    # Generate one docker run block per container
    for idx, image in enumerate(images):
        name = names[idx]
        hp = host_ports[idx]
        cp = container_ports[idx]
        vol = volumes[idx].strip()
        envs = env_lists[idx].strip().splitlines()

        run_cmd = f"docker run -d --name {name} -p {hp}:{cp}"
        if vol:
            run_cmd += f" -v {vol}"
        for env in envs:
            if env.strip():
                run_cmd += f" -e {env.strip()}"
        run_cmd += f" {image}"
        lines.append(f"# Container {idx+1}: {name}")
        lines.append(run_cmd)
        lines.append("")

    return "\n".join(lines)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        images = request.form.getlist("image_name[]")
        names = request.form.getlist("container_name[]")
        host_ports = request.form.getlist("host_port[]")
        container_ports = request.form.getlist("container_port[]")
        volumes = request.form.getlist("volume_mapping[]")
        # For env vars we collect a list of multiline strings
        env_lists = request.form.getlist("env_vars[]")

        script = generate_bash_script(images, names, host_ports, container_ports, volumes, env_lists)
        buffer = BytesIO(script.encode())
        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name="setup.sh",
            mimetype="text/x-sh",
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
