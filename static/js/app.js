let appData = { profil: {}, kegiatan: [] };

document.addEventListener('DOMContentLoaded', () => {
    // --- Tabs Logic ---
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.add('hidden'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            const target = document.getElementById(btn.dataset.target);
            target.classList.remove('hidden');
            target.classList.add('active');
        });
    });

    // --- Populate Select Minggu ---
    const selectMingguFilter = document.getElementById('filterMinggu');
    const selectMingguForm = document.getElementById('minggu');
    if (selectMingguForm) {
        for (let i = 1; i <= 24; i++) {
            const opt = new Option(`Minggu ${i}`, i);
            selectMingguForm.add(opt);
            
            const optFilter = new Option(`Minggu ${i}`, i);
            selectMingguFilter.add(optFilter);
        }
    }

    // --- Load Data ---
    async function loadData() {
        try {
            const res = await fetch('/api/data');
            if (res.ok) {
                appData = await res.json();
                if (!appData.profil) appData.profil = {};
                if (!appData.kegiatan) appData.kegiatan = [];
                renderProfil();
                renderKegiatan();
                updateExportStats();
            }
        } catch (err) {
            console.error("Gagal load data", err);
        }
    }
    
    // --- Save Data ---
    async function saveData() {
        try {
            await fetch('/api/data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(appData)
            });
            updateExportStats();
        } catch (err) {
            console.error("Gagal save data", err);
        }
    }

    // --- Profil Form ---
    const profilForm = document.getElementById('profilForm');
    if (profilForm) {
        const profilFields = ['nama', 'nim', 'prodi', 'fakultas', 'universitas', 'perusahaan', 'alamat_perusahaan', 'periode_mulai', 'periode_selesai', 'dosen_pembimbing', 'pembimbing_lapangan'];
        
        window.renderProfil = () => {
            profilFields.forEach(f => {
                const el = document.getElementById(`p_${f}`);
                if (el) el.value = appData.profil[f] || '';
            });
        };

        profilForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            profilFields.forEach(f => {
                const el = document.getElementById(`p_${f}`);
                if (el) appData.profil[f] = el.value.trim();
            });
            await saveData();
            alert("Profil berhasil disimpan!");
        });
    }

    // --- Kegiatan Form & Table ---
    const kegiatanForm = document.getElementById('kegiatanForm');
    if (kegiatanForm) {
        window.renderKegiatan = () => {
            const tbody = document.getElementById('kegiatanTbody');
            tbody.innerHTML = '';
            
            const query = document.getElementById('searchInput').value.toLowerCase();
            const filterMinggu = document.getElementById('filterMinggu').value;
            
            let displayed = 0;
            
            appData.kegiatan.forEach((k, idx) => {
                const matchQuery = !query || k.kegiatan.toLowerCase().includes(query) || k.keterangan.toLowerCase().includes(query) || k.tanggal.toLowerCase().includes(query);
                const matchMinggu = filterMinggu === 'Semua' || k.minggu == filterMinggu;
                
                if (matchQuery && matchMinggu) {
                    displayed++;
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${idx + 1}</td>
                        <td>${k.tanggal}</td>
                        <td>Minggu ${k.minggu}</td>
                        <td>${k.kegiatan}</td>
                        <td>${k.keterangan}</td>
                        <td>
                            <div class="flex-row gap-2">
                                <button class="btn btn-warning btn-sm" onclick="editKegiatan(${idx})" style="padding:5px;">✏️</button>
                                <button class="btn btn-danger btn-sm" onclick="deleteKegiatan(${idx})" style="padding:5px;">🗑️</button>
                            </div>
                        </td>
                    `;
                    tbody.appendChild(tr);
                }
            });
            
            document.getElementById('tableStatus').textContent = `Menampilkan ${displayed} dari ${appData.kegiatan.length} kegiatan`;
        };
        
        document.getElementById('searchInput').addEventListener('input', renderKegiatan);
        document.getElementById('filterMinggu').addEventListener('change', renderKegiatan);
        document.getElementById('resetFilterBtn').addEventListener('click', () => {
            document.getElementById('searchInput').value = '';
            document.getElementById('filterMinggu').value = 'Semua';
            renderKegiatan();
        });

        kegiatanForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const editIdx = parseInt(document.getElementById('editIndex').value);
            const entry = {
                tanggal: document.getElementById('tanggal').value.trim(),
                minggu: document.getElementById('minggu').value,
                kegiatan: document.getElementById('kegiatan').value.trim(),
                keterangan: document.getElementById('keterangan').value.trim()
            };
            
            if (editIdx >= 0) {
                appData.kegiatan[editIdx] = entry;
                document.getElementById('cancelEditBtn').click();
            } else {
                appData.kegiatan.push(entry);
            }
            
            kegiatanForm.reset();
            renderKegiatan();
            await saveData();
        });

        document.getElementById('cancelEditBtn').addEventListener('click', () => {
            kegiatanForm.reset();
            document.getElementById('editIndex').value = -1;
            document.getElementById('saveKegiatanBtn').innerHTML = '➕ Simpan Kegiatan';
            document.getElementById('formKegiatanTitle').textContent = 'Tambah Kegiatan';
            document.getElementById('cancelEditBtn').classList.add('hidden');
        });
        
        window.editKegiatan = (idx) => {
            const k = appData.kegiatan[idx];
            document.getElementById('tanggal').value = k.tanggal;
            document.getElementById('minggu').value = k.minggu;
            document.getElementById('kegiatan').value = k.kegiatan;
            document.getElementById('keterangan').value = k.keterangan;
            document.getElementById('editIndex').value = idx;
            
            document.getElementById('saveKegiatanBtn').innerHTML = '✏️ Update Kegiatan';
            document.getElementById('formKegiatanTitle').textContent = 'Edit Kegiatan';
            document.getElementById('cancelEditBtn').classList.remove('hidden');
        };
        
        window.deleteKegiatan = async (idx) => {
            if (confirm('Yakin hapus kegiatan ini?')) {
                appData.kegiatan.splice(idx, 1);
                renderKegiatan();
                await saveData();
            }
        };
    }
    
    // --- Export ---
    function updateExportStats() {
        const stats = document.getElementById('exportStats');
        if (stats) {
            const p = appData.profil;
            const k = appData.kegiatan;
            const weeks = new Set(k.map(x => x.minggu)).size;
            stats.innerHTML = `
                Nama: ${p.nama || '-'}<br>
                Perusahaan: ${p.perusahaan || '-'}<br>
                Total Kegiatan: ${k.length} | Jumlah Minggu: ${weeks}
            `;
        }
    }

    // --- Password ---
    const pwdForm = document.getElementById('passwordForm');
    if (pwdForm) {
        pwdForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const old_pwd = document.getElementById('old_pwd').value;
            const new_pwd = document.getElementById('new_pwd').value;
            const confirm_pwd = document.getElementById('confirm_pwd').value;
            
            if (new_pwd !== confirm_pwd) {
                alert("Password baru dan konfirmasi tidak sama!");
                return;
            }
            
            try {
                const res = await fetch('/api/change_password', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ old_pwd, new_pwd })
                });
                const data = await res.json();
                alert(data.message);
                if(data.success) pwdForm.reset();
            } catch(e) {
                alert("Terjadi kesalahan.");
            }
        });
    }

    // Initialize
    loadData();
});
