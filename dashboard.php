<?php
include 'auth.php';
$db = new PDO('sqlite:verifyme.sqlite');
$users = $db->query("SELECT * FROM users ORDER BY created_at DESC")->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html>
<head><title>Admin Dashboard</title></head>
<body>
<h2>✅ Verified ID Submissions</h2>
<a href="logout.php">Logout</a>
<table border="1" cellpadding="5" cellspacing="0">
<tr><th>ID</th><th>Username</th><th>Email</th><th>ID Image</th><th>Status</th><th>Notes</th><th>Submitted At</th></tr>
<?php foreach ($users as $user): ?>
<tr>
<td><?= htmlspecialchars($user['id']) ?></td>
<td><?= htmlspecialchars($user['username']) ?></td>
<td><?= htmlspecialchars($user['email']) ?></td>
<td><img src="<?= htmlspecialchars($user['id_image']) ?>" width="100"></td>
<td><?= htmlspecialchars($user['status']) ?></td>
<td><?= htmlspecialchars($user['notes']) ?></td>
<td><?= htmlspecialchars($user['created_at']) ?></td>
</tr>
<?php endforeach; ?>
</table>
</body>
</html>
