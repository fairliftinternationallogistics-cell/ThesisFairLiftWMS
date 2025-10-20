<?php
// Main dashboard page (warehouse.php) - drop into XAMPP htdocs/fairlift_warehouse/
// Expects db.php, fetch_parcels.php, add_parcel.php, update_status.php next to it.
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>FairLift — Warehouse Monitoring</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />

  <!-- Bootstrap Icons -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">

  <style>
    :root {
      --bg:#ffffff;
      --sidebar:#A3001E;
      --sidebar-text:#fff;
      --accent:#A3001E;
      --card:#fafafa;
      --muted:#666;
      font-family: 'Inter', sans-serif;
    }

    * { box-sizing:border-box; }

    html,body {
      margin:0;
      padding:0;
      height:100%;
      background:var(--bg);
      color:#222;
      font-family:'Inter',sans-serif;
      display:flex;
    }

    /* Sidebar */
    .sidebar {
      width:230px;
      background:var(--sidebar);
      color:#fff;
      display:flex;
      flex-direction:column;
      height:100vh;
      position:fixed;
      top:0;
      left:0;
      padding:25px 15px;
      box-shadow:2px 0 8px rgba(0,0,0,0.15);
    }

    .sidebar h2 {
      font-size:20px;
      font-weight:700;
      letter-spacing:1px;
      margin-bottom:25px;
      text-align:center;
      text-transform:uppercase;
      color:#fff;
    }

    .nav-link {
      color:#fff;
      display:flex;
      align-items:center;
      padding:12px 14px;
      border-radius:8px;
      margin:5px 0;
      font-weight:500;
      text-decoration:none;
      transition:0.25s;
    }

    .nav-link i {
      margin-right:12px;
      font-size:1.1rem;
    }

    .nav-link:hover {
      background:rgba(255,255,255,0.2);
      transform:translateX(3px);
    }

    .nav-link.active {
      background:#fff;
      color:var(--accent);
      font-weight:600;
    }

    .spacer {
      flex-grow:1;
    }

    .logout {
      background:rgba(255,255,255,0.2);
      text-align:center;
      padding:10px;
      border-radius:6px;
      color:#fff;
      text-decoration:none;
      transition:0.2s;
    }

    .logout:hover {
      background:rgba(255,255,255,0.3);
    }

    /* Main content */
    .main {
      margin-left:230px;
      flex-grow:1;
      display:flex;
      flex-direction:column;
      min-height:100vh;
      background:#fff;
    }

    header {
      background:white;
      padding:20px 30px;
      display:flex;
      justify-content:space-between;
      align-items:center;
      border-bottom:1px solid #eee;
    }

    header h1 {
      margin:0;
      color:var(--accent);
      font-size:20px;
    }

    header p {
      color:#666;
      font-size:13px;
      margin:4px 0 0;
    }

    .table-actions {
      display:flex;
      gap:10px;
      align-items:center;
    }

    .btn {
      background:var(--accent);
      color:white;
      border:none;
      padding:8px 14px;
      border-radius:6px;
      cursor:pointer;
      font-size:14px;
    }

    .ghost {
      background:white;
      border:1px solid #ccc;
      color:#333;
      padding:8px 12px;
      border-radius:6px;
      cursor:pointer;
    }

    .export-btn {
      background:#fff;
      border:1px solid #ccc;
      padding:7px 10px;
      border-radius:6px;
      cursor:pointer;
      color:#333;
    }

    .content {
      padding:25px 40px;
      flex-grow:1;
      background:#fafafa;
    }

    .card {
      background:white;
      border-radius:10px;
      padding:20px;
      box-shadow:0 2px 10px rgba(0,0,0,0.05);
    }

    .controls {
      display:flex;
      flex-wrap:wrap;
      gap:15px;
      margin-bottom:15px;
    }

    .controls div {
      background:#fff;
      border:1px solid #ddd;
      border-radius:8px;
      padding:6px 10px;
    }

    .controls input, .controls select {
      border:none;
      outline:none;
      font-size:14px;
      background:transparent;
      min-width:120px;
    }

    table {
      width:100%;
      border-collapse:collapse;
      margin-top:10px;
      font-size:14px;
    }

    th, td {
      text-align:left;
      padding:10px;
      border-bottom:1px solid #eee;
    }

    th {
      background:#f9f9f9;
      cursor:pointer;
      color:#444;
    }

    tr:hover { background:#fff3f3; }

    .badge {
      padding:4px 8px;
      border-radius:999px;
      font-size:12px;
      display:inline-block;
    }

    .badge.stored { background:#e9ecef; color:#333; }
    .badge.shipped { background:#27ae60; color:white; }
    .badge.pending { background:#f39c12; color:white; }

    footer {
      text-align:center;
      color:#777;
      padding:10px;
      font-size:13px;
    }

    /* Modal */
    .modal {
      position:fixed;
      left:0; top:0; right:0; bottom:0;
      background:rgba(0,0,0,0.5);
      display:none;
      align-items:center;
      justify-content:center;
      z-index:50;
    }

    .modal.show { display:flex; }

    .modal-card {
      background:white;
      padding:20px;
      border-radius:10px;
      width:700px;
      max-width:95%;
      border-top:6px solid var(--accent);
      box-shadow:0 10px 40px rgba(0,0,0,0.2);
    }

    .row { display:flex; flex-wrap:wrap; gap:10px; margin-top:5px; }
    .col { flex:1; }

    .actions { display:flex; justify-content:flex-end; gap:8px; margin-top:15px; }

    @media (max-width:768px) {
      .sidebar { width:100%; height:auto; position:relative; flex-direction:row; flex-wrap:wrap; justify-content:center; }
      .main { margin-left:0; }
    }

    .form-field { margin-bottom:8px; }
    .form-field input, .form-field select { width:100%; padding:8px; border:1px solid #ddd; border-radius:6px; }
  </style>
</head>
<body>
  <!-- Sidebar -->
  <nav class="sidebar">
    <h2>FAIRLIFT</h2>
    <a href="#" class="nav-link"><i class="bi bi-speedometer2"></i> Dashboard</a>
    <a href="#" class="nav-link"><i class="bi bi-calendar3"></i> Calendar</a>
    <a href="#" class="nav-link"><i class="bi bi-geo-alt"></i> Tracking</a>
    <a href="#" class="nav-link active"><i class="bi bi-box-seam"></i> Warehouse</a>
    <a href="#" class="nav-link"><i class="bi bi-truck"></i> Orders</a>
    <a href="#" class="nav-link"><i class="bi bi-gear"></i> Settings</a>
    <a href="#" class="nav-link"><i class="bi bi-question-circle"></i> Help Center</a>
    <div class="spacer"></div>
    <a href="#" class="logout"><i class="bi bi-house-door"></i> Home</a>
  </nav>

  <!-- Main content -->
  <div class="main">
    <header>
      <div>
        <h1>Warehouse Monitoring</h1>
        <p>View parcels, sort by size/date/destination, open details, and export lists.</p>
      </div>
      <div class="table-actions">
        <button id="exportCsv" class="export-btn">Export CSV</button>
        <button id="bulkPrint" class="ghost">Bulk Print</button>
        <button id="addParcelBtn" class="btn">Add Parcel</button>
      </div>
    </header>

    <div class="content">
      <div class="card">
        <div class="controls">
          <div><input id="search" type="text" placeholder="Search tracking or destination"></div>
          <div><select id="filterSize"><option value="">All Sizes</option><option>S</option><option>M</option><option>L</option><option>XL</option></select></div>
          <div><input id="filterDestination" type="text" placeholder="Destination"></div>
          <div><input id="dateFrom" type="date"></div>
          <div><input id="dateTo" type="date"></div>
        </div>

        <table id="parcelsTable">
          <thead>
            <tr>
              <th>Tracking #</th>
              <th>Size</th>
              <th>Weight (kg)</th>
              <th>Arrival Date</th>
              <th>Destination</th>
              <th>Status</th>
              <th>Location</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="tableBody"></tbody>
        </table>
      </div>
    </div>

    <footer>© 2025 FairLift International Logistics, Inc.</footer>
  </div>

  <!-- Modal: Parcel Details -->
  <div id="modal" class="modal">
    <div class="modal-card">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2 id="modalTitle" style="color:var(--accent); margin:0;">Parcel Details</h2>
        <button id="closeModal" class="ghost">Close</button>
      </div>
      <hr style="margin:10px 0; border:1px solid #eee;">
      <div id="modalContent"></div>
      <div class="actions">
        <button id="createTicket" class="btn">Create Ticket</button>
        <button id="markShipped" class="ghost">Mark Shipped</button>
      </div>
    </div>
  </div>

  <!-- Modal: Add Parcel -->
  <div id="addModal" class="modal">
    <div class="modal-card">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2 style="color:var(--accent); margin:0;">Add Parcel</h2>
        <button id="closeAddModal" class="ghost">Close</button>
      </div>
      <hr style="margin:10px 0; border:1px solid #eee;">
      <div id="addContent">
        <div class="form-field"><label>Tracking #</label><input id="inpTracking" /></div>
        <div class="form-field"><label>Size</label><select id="inpSize"><option>S</option><option>M</option><option>L</option><option>XL</option></select></div>
        <div class="form-field"><label>Weight (kg)</label><input id="inpWeight" type="number" step="0.01" /></div>
        <div class="form-field"><label>Arrival Date</label><input id="inpArrival" type="date" /></div>
        <div class="form-field"><label>Destination</label><input id="inpDestination" /></div>
        <div class="form-field"><label>Location Rack</label><input id="inpRack" /></div>
        <div class="form-field"><label>Status</label><select id="inpStatus"><option value="stored">stored</option><option value="pending">pending</option><option value="shipped">shipped</option></select></div>
      </div>
      <div class="actions">
        <button id="saveParcel" class="btn">Save Parcel</button>
      </div>
    </div>
  </div>

  <script>
    const tableBody = document.getElementById('tableBody');
    const modal = document.getElementById('modal');
    const modalContent = document.getElementById('modalContent');
    const closeModal = document.getElementById('closeModal');

    const addModal = document.getElementById('addModal');
    const addParcelBtn = document.getElementById('addParcelBtn');
    const closeAddModal = document.getElementById('closeAddModal');
    const saveParcelBtn = document.getElementById('saveParcel');

    let parcels = [];

    async function loadParcels() {
      try {
        const res = await fetch('fetch_parcels.php');
        parcels = await res.json();
        renderTable();
      } catch (err) {
        console.error(err);
        tableBody.innerHTML = '<tr><td colspan="8">Unable to load parcels. Check fetch_parcels.php and DB connection.</td></tr>';
      }
    }

    function renderTable() {
      tableBody.innerHTML = '';
      if (!Array.isArray(parcels) || parcels.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="8">No parcels found.</td></tr>';
        return;
      }
      parcels.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${p.tracking_number}</td>
          <td>${p.size}</td>
          <td>${p.weight}</td>
          <td>${p.arrival_date}</td>
          <td>${p.destination}</td>
          <td><span class="badge ${p.status}">${p.status}</span></td>
          <td>${p.location_rack}</td>
          <td>
            <button class="ghost" onclick="openModal('${p.id}')">Open</button>
            <button class="ghost" onclick="markShipped('${p.id}')">Mark Shipped</button>
          </td>
        `;
        tableBody.appendChild(tr);
      });
    }

    window.openModal = function(id) {
      const p = parcels.find(x => x.id === id);
      if (!p) return;
      modalContent.innerHTML = `
        <div class="row"><div class="col"><b>Tracking #:</b> ${p.tracking_number}</div><div class="col"><b>Destination:</b> ${p.destination}</div></div>
        <div class="row"><div class="col"><b>Size:</b> ${p.size}</div><div class="col"><b>Weight:</b> ${p.weight} kg</div></div>
        <div class="row"><div class="col"><b>Arrival:</b> ${p.arrival_date}</div><div class="col"><b>Location:</b> ${p.location_rack}</div></div>
        <div style="margin-top:10px;"><b>Status:</b> <span class="badge ${p.status}">${p.status}</span></div>
      `;
      modal.classList.add('show');
    }

    closeModal.onclick = () => modal.classList.remove('show');
    window.onclick = e => { if (e.target === modal) modal.classList.remove('show'); }

    // Add parcel modal
    addParcelBtn.onclick = () => addModal.classList.add('show');
    closeAddModal.onclick = () => addModal.classList.remove('show');
    window.addEventListener('keydown', e => {
      if (e.key === 'Escape') { modal.classList.remove('show'); addModal.classList.remove('show'); }
    });

    saveParcelBtn.onclick = async () => {
      const data = {
        tracking_number: document.getElementById('inpTracking').value.trim(),
        size: document.getElementById('inpSize').value,
        weight: document.getElementById('inpWeight').value,
        arrival_date: document.getElementById('inpArrival').value,
        destination: document.getElementById('inpDestination').value.trim(),
        location_rack: document.getElementById('inpRack').value.trim(),
        status: document.getElementById('inpStatus').value
      };
      // basic validation
      if (!data.tracking_number || !data.destination) {
        alert('Please provide at least Tracking # and Destination.');
        return;
      }
      try {
        const res = await fetch('add_parcel.php', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify(data)
        });
        const json = await res.json();
        if (json.success) {
          addModal.classList.remove('show');
          await loadParcels();
        } else {
          alert('Error: ' + (json.error || 'Unknown'));
        }
      } catch (err) {
        alert('Request failed. Check server logs.');
        console.error(err);
      }
    };

    // Mark shipped (quick action)
    window.markShipped = async function(id) {
      if (!confirm('Mark parcel as shipped?')) return;
      try {
        const res = await fetch('update_status.php', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ id: id, status: 'shipped' })
        });
        const json = await res.json();
        if (json.success) {
          await loadParcels();
        } else {
          alert('Update failed: ' + (json.error || 'Unknown'));
        }
      } catch (err) {
        alert('Request failed.');
        console.error(err);
      }
    };

    // CSV export (client-side)
    document.getElementById('exportCsv').onclick = function() {
      if (!parcels.length) { alert('No data to export'); return; }
      const header = ['id','tracking_number','size','weight','arrival_date','destination','status','location_rack'];
      const rows = parcels.map(p => header.map(h => '"' + (p[h] ?? '') + '"').join(','));
      const csv = [header.join(','), ...rows].join('\n');
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'parcels_export.csv';
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    };

    // initial load
    loadParcels();
  </script>
</body>
</html>
