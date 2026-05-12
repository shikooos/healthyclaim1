<?php
header('Content-Type: application/json');

// Config
$to = 'info@healthyclaim.com';
$allowed_types = ['demo', 'investor'];

// Validate inputs
$form_type = isset($_POST['form_type']) && in_array($_POST['form_type'], $allowed_types)
    ? $_POST['form_type'] : 'general';

$name    = htmlspecialchars(strip_tags(trim($_POST['name'] ?? '')));
$email   = filter_var(trim($_POST['email'] ?? ''), FILTER_SANITIZE_EMAIL);
$org     = htmlspecialchars(strip_tags(trim($_POST['organization'] ?? '')));
$message = htmlspecialchars(strip_tags(trim($_POST['message'] ?? '')));
$role    = htmlspecialchars(strip_tags(trim($_POST['role'] ?? $_POST['investor_type'] ?? '')));

if (empty($name) || empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo json_encode(['success' => false, 'message' => 'Please provide a valid name and email address.']);
    exit;
}

// Build email
if ($form_type === 'investor') {
    $subject = "[INVESTOR INQUIRY] $name - $org";
    $body = "New Investor Inquiry via HealthyClaim.com\n";
    $body .= str_repeat('=', 50) . "\n\n";
    $body .= "Name:           $name\n";
    $body .= "Email:          $email\n";
    $body .= "Firm/Org:       $org\n";
    $body .= "Investor Type:  $role\n\n";
    $body .= "Message:\n$message\n\n";
    $body .= str_repeat('-', 50) . "\n";
    $body .= "Sent from: healthyclaim.com | " . date('Y-m-d H:i:s T');
    $success_msg = "Thank you for your interest in HealthyClaim! We've received your investor inquiry and will be in touch very soon.";
} else {
    $subject = "[DEMO REQUEST] $name - $org";
    $body = "New Demo Waitlist Signup via HealthyClaim.com\n";
    $body .= str_repeat('=', 50) . "\n\n";
    $body .= "Name:           $name\n";
    $body .= "Email:          $email\n";
    $body .= "Organization:   $org\n";
    $body .= "Role:           $role\n\n";
    $body .= "Message / Needs:\n$message\n\n";
    $body .= str_repeat('-', 50) . "\n";
    $body .= "Sent from: healthyclaim.com | " . date('Y-m-d H:i:s T');
    $success_msg = "You're on the list! We'll contact you at $email to schedule your personalized HealthyClaim demo.";
}

// Mail headers
$headers  = "From: HealthyClaim Website <noreply@healthyclaim.com>\r\n";
$headers .= "Reply-To: $name <$email>\r\n";
$headers .= "X-Mailer: PHP/" . phpversion();

// Send
if (mail($to, $subject, $body, $headers)) {
    echo json_encode(['success' => true, 'message' => $success_msg]);
} else {
    echo json_encode(['success' => false, 'message' => 'Sorry, there was a sending error. Please email us directly at info@healthyclaim.com']);
}
exit;
