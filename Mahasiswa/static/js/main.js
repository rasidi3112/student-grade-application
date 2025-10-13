// Background animation with Three.js
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('bg-animation')) {
        initBackgroundAnimation();
    }
    
    // Load stats for dashboard or grades page
    fetchAndDisplayStats();
    
    // Setup modal events if modal exists
    setupModalEvents();
});

function initBackgroundAnimation() {
    const canvas = document.getElementById('bg-animation');
    
    // Three.js scene setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    
    const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        alpha: true,
        antialias: true
    });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    
    // Create particles
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 1000;
    
    const positions = new Float32Array(particlesCount * 3);
    const colors = new Float32Array(particlesCount * 3);
    
    const colorOptions = [
        new THREE.Color(0x4f46e5), // primary
        new THREE.Color(0x7c3aed), // secondary
        new THREE.Color(0xc026d3)  // accent
    ];
    
    for (let i = 0; i < particlesCount; i++) {
        // Position
        positions[i * 3] = (Math.random() - 0.5) * 10;
        positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
        positions[i * 3 + 2] = (Math.random() - 0.5) * 10;
        
        // Color
        const color = colorOptions[Math.floor(Math.random() * colorOptions.length)];
        colors[i * 3] = color.r;
        colors[i * 3 + 1] = color.g;
        colors[i * 3 + 2] = color.b;
    }
    
    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    
    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.015,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        sizeAttenuation: true
    });
    
    const particles = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particles);
    
    camera.position.z = 5;
    
    // Animation loop
    const animate = () => {
        requestAnimationFrame(animate);
        
        particles.rotation.x += 0.0005;
        particles.rotation.y += 0.0005;
        
        // Move camera slightly to create gentle movement
        camera.position.x = Math.sin(Date.now() * 0.0001) * 0.2;
        camera.position.y = Math.cos(Date.now() * 0.0001) * 0.1;
        
        renderer.render(scene, camera);
    };
    
    animate();
    
    // Handle window resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

function fetchAndDisplayStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            // Update dashboard or grades page stats
            const averageElement = document.getElementById('average-grade');
            const highestElement = document.getElementById('highest-grade');
            const lowestElement = document.getElementById('lowest-grade');
            const totalElement = document.getElementById('total-students');
            
            if (averageElement) averageElement.textContent = data.average.toFixed(2);
            if (highestElement) highestElement.textContent = data.highest;
            if (lowestElement) lowestElement.textContent = data.lowest;
            if (totalElement) totalElement.textContent = data.count;
        })
        .catch(error => console.error('Error fetching stats:', error));
}

function setupModalEvents() {
    const modal = document.getElementById('stats-modal');
    const closeButton = document.getElementById('modal-close');
    const statBoxes = document.querySelectorAll('.stat-box');
    
    if (!modal || !closeButton) return;
    
    // Add click event to stat boxes
    statBoxes.forEach(box => {
        box.addEventListener('click', () => {
            const statType = box.id.replace('-stat', '');
            const modalTitle = document.getElementById('modal-title');
            const modalContent = document.getElementById('modal-content');
            
            // Set modal title and content based on clicked stat
            switch (statType) {
                case 'average':
                    modalTitle.textContent = 'Detail Rata-rata Nilai';
                    displayAverageDetails(modalContent);
                    break;
                case 'highest':
                    modalTitle.textContent = 'Detail Nilai Tertinggi';
                    displayHighestDetails(modalContent);
                    break;
                case 'lowest':
                    modalTitle.textContent = 'Detail Nilai Terendah';
                    displayLowestDetails(modalContent);
                    break;
                case 'total':
                    modalTitle.textContent = 'Detail Total Mahasiswa';
                    displayTotalDetails(modalContent);
                    break;
            }
            
            // Show modal
            modal.classList.add('active');
        });
    });
    
    // Close modal on button click
    closeButton.addEventListener('click', () => {
        modal.classList.remove('active');
    });
    
    // Close modal when clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
}

function displayAverageDetails(contentElement) {
    fetch('/api/students')
        .then(response => response.json())
        .then(students => {
            if (students.length === 0) {
                contentElement.innerHTML = '<p>Belum ada data untuk ditampilkan.</p>';
                return;
            }
            
            // Calculate average per semester
            const semesterStats = {};
            students.forEach(student => {
                if (!semesterStats[student.semester]) {
                    semesterStats[student.semester] = {
                        total: 0,
                        count: 0
                    };
                }
                
                semesterStats[student.semester].total += student.grade;
                semesterStats[student.semester].count += 1;
            });
            
            let content = `
                <p>Rata-rata nilai dihitung dari ${students.length} data nilai mahasiswa.</p>
                <h3>Rata-rata Nilai Per Semester</h3>
                <div class="top-list">
            `;
            
            for (const semester in semesterStats) {
                const average = (semesterStats[semester].total / semesterStats[semester].count).toFixed(2);
                content += `
                    <div class="top-list-item">
                        <span>${semester}</span>
                        <span>${average}</span>
                    </div>
                `;
            }
            
            content += '</div>';
            contentElement.innerHTML = content;
        })
        .catch(error => {
            console.error('Error:', error);
            contentElement.innerHTML = '<p>Terjadi kesalahan saat memuat data.</p>';
        });
}

function displayHighestDetails(contentElement) {
    fetch('/api/students')
        .then(response => response.json())
        .then(students => {
            if (students.length === 0) {
                contentElement.innerHTML = '<p>Belum ada data untuk ditampilkan.</p>';
                return;
            }
            
            // Get top 5 students
            const topStudents = [...students].sort((a, b) => b.grade - a.grade).slice(0, 5);
            
            let content = `
                <p>Berikut adalah 5 mahasiswa dengan nilai tertinggi:</p>
                <div class="top-list">
            `;
            
            topStudents.forEach((student, index) => {
                const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '';
                
                content += `
                    <div class="top-list-item">
                        <span><span class="top-list-medal">${medal}</span> ${student.name} (${student.course})</span>
                        <span>${student.grade}</span>
                    </div>
                `;
            });
            
            content += '</div>';
            contentElement.innerHTML = content;
        })
        .catch(error => {
            console.error('Error:', error);
            contentElement.innerHTML = '<p>Terjadi kesalahan saat memuat data.</p>';
        });
}

function displayLowestDetails(contentElement) {
    fetch('/api/students')
        .then(response => response.json())
        .then(students => {
            if (students.length === 0) {
                contentElement.innerHTML = '<p>Belum ada data untuk ditampilkan.</p>';
                return;
            }
            
            // Get 5 students with lowest grades
            const lowestStudents = [...students].sort((a, b) => a.grade - b.grade).slice(0, 5);
            
            let content = `
                <p>Berikut adalah 5 mahasiswa dengan nilai terendah:</p>
                <div class="top-list">
            `;
            
            lowestStudents.forEach((student, index) => {
                content += `
                    <div class="top-list-item">
                        <span>${student.name} (${student.course})</span>
                        <span>${student.grade}</span>
                    </div>
                `;
            });
            
            content += '</div>';
            
            // Add recommendation
            content += `
                <h3>Rekomendasi</h3>
                <p>Mahasiswa dengan nilai di bawah 55 disarankan untuk mengikuti pemebelajaran tambahan atau remedial guna meningkatkan pemahaman terhadap materi yang telah di ajarkan.</p>
            `;
            
            contentElement.innerHTML = content;
        })
        .catch(error => {
            console.error('Error:', error);
            contentElement.innerHTML = '<p>Terjadi kesalahan saat memuat data.</p>';
        });
}

function displayTotalDetails(contentElement) {
    fetch('/api/students')
        .then(response => response.json())
        .then(students => {
            if (students.length === 0) {
                contentElement.innerHTML = '<p>Belum ada data untuk ditampilkan.</p>';
                return;
            }
            
            // Count students per semester
            const semesterCount = {};
            students.forEach(student => {
                if (!semesterCount[student.semester]) {
                    semesterCount[student.semester] = 0;
                }
                semesterCount[student.semester]++;
            });
            
            // Count students per course
            const courseCount = {};
            students.forEach(student => {
                if (!courseCount[student.course]) {
                    courseCount[student.course] = 0;
                }
                courseCount[student.course]++;
            });
            
            let content = `
                <p>Total <span class="highlight">${students.length}</span> data nilai mahasiswa telah direkam dalam sistem.</p>
                
                <h3>Jumlah Data per Semester</h3>
                <div class="top-list">
            `;
            
            for (const semester in semesterCount) {
                content += `
                    <div class="top-list-item">
                        <span>${semester}</span>
                        <span>${semesterCount[semester]} mahasiswa</span>
                    </div>
                `;
            }
            
            content += `
                </div>
                
                <h3>Jumlah Data per Mata Kuliah</h3>
                <div class="top-list">
            `;
            
            for (const course in courseCount) {
                content += `
                    <div class="top-list-item">
                        <span>${course}</span>
                        <span>${courseCount[course]} mahasiswa</span>
                    </div>
                `;
            }
            
            content += '</div>';
            contentElement.innerHTML = content;
        })
        .catch(error => {
            console.error('Error:', error);
            contentElement.innerHTML = '<p>Terjadi kesalahan saat memuat data.</p>';
        });
}