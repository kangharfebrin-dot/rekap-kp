document.addEventListener('DOMContentLoaded', () => {
    async function loadUsers() {
        try {
            const res = await fetch('/api/admin/users');
            const users = await res.json();
            
            const tbody = document.getElementById('adminUsersTbody');
            tbody.innerHTML = '';
            
            users.forEach(u => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${u.username}</td>
                    <td><span style="padding:4px 8px; border-radius:4px; background:${u.role==='admin'?'var(--danger-color)':'var(--success-color)'}; color:white; font-size:12px;">${u.role}</span></td>
                    <td>${u.nama || '-'}</td>
                    <td>${u.nim || '-'}</td>
                    <td>${u.perusahaan || '-'}</td>
                    <td>${u.jml_keg}</td>
                    <td>
                        <button class="btn btn-warning btn-sm" onclick="editUser('${u.username}', '${u.role}')" style="padding:4px 8px;">✏️</button>
                        <button class="btn btn-danger btn-sm" onclick="deleteUser('${u.username}')" style="padding:4px 8px;">🗑️</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        } catch (err) {
            console.error("Gagal memuat users", err);
        }
    }

    const form = document.getElementById('adminUserForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('a_username').value;
        const password = document.getElementById('a_password').value;
        const role = document.getElementById('a_role').value;
        
        const isUpdate = document.getElementById('a_username').disabled;
        const method = isUpdate ? 'PUT' : 'POST';
        
        try {
            const res = await fetch('/api/admin/users', {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password, role })
            });
            const data = await res.json();
            
            alert(data.message);
            if(data.success) {
                document.getElementById('cancelUserEditBtn').click();
                loadUsers();
            }
        } catch (e) {
            alert('Terjadi kesalahan jaringan.');
        }
    });

    document.getElementById('cancelUserEditBtn').addEventListener('click', () => {
        form.reset();
        document.getElementById('a_username').disabled = false;
        document.getElementById('formUserTitle').textContent = '➕ Tambah Pengguna Baru';
        document.getElementById('cancelUserEditBtn').classList.add('hidden');
    });

    window.editUser = (username, role) => {
        document.getElementById('a_username').value = username;
        document.getElementById('a_username').disabled = true; // prevent changing pk
        document.getElementById('a_role').value = role;
        document.getElementById('a_password').value = '';
        
        document.getElementById('formUserTitle').textContent = `✏️ Edit Pengguna: ${username}`;
        document.getElementById('cancelUserEditBtn').classList.remove('hidden');
    };

    window.deleteUser = async (username) => {
        if(confirm(`Yakin hapus akun ${username}?`)) {
            try {
                const res = await fetch(`/api/admin/users/${username}`, { method: 'DELETE' });
                const data = await res.json();
                alert(data.message);
                if(data.success) loadUsers();
            } catch (e) {
                alert('Gagal menghapus user.');
            }
        }
    };

    loadUsers();
});
