document.addEventListener('DOMContentLoaded', function () {
  const category = document.getElementById('category');
  const dynamicFields = document.getElementById('dynamic-fields');

  if (!category) return;

  category.addEventListener('change', function () {
    dynamicFields.innerHTML = '';

    switch (category.value) {
      case 'Profession':
        dynamicFields.innerHTML = `
          <label>Full Name:</label>
          <input type="text" name="full_name" required>

          <label>ID Number:</label>
          <input type="text" name="id_number" required>

          <label>Varsity/College:</label>
          <input type="text" name="college" required>

          <label>Upload Certificate:</label>
          <input type="file" name="certificate" required>

          <label>Upload ID Copy:</label>
          <input type="file" name="id_copy" required>

          <label>Attendance Record:</label>
          <input type="file" name="attendance">
        `;
        break;

      case 'Car':
        dynamicFields.innerHTML = `
          <label>Owner Name:</label>
          <input type="text" name="owner_name" required>

          <label>Registration Number:</label>
          <input type="text" name="reg_number" required>

          <label>Make / Model:</label>
          <input type="text" name="make_model" required>

          <label>Registration Document:</label>
          <input type="file" name="reg_doc" required>
        `;
        break;

      case 'Stand':
        dynamicFields.innerHTML = `
          <label>Owner Name:</label>
          <input type="text" name="owner_name" required>

          <label>Stand Number:</label>
          <input type="text" name="stand_number" required>

          <label>Location:</label>
          <input type="text" name="location" required>

          <label>Proof of Ownership:</label>
          <input type="file" name="ownership_doc" required>
        `;
        break;

      case 'House':
        dynamicFields.innerHTML = `
          <label>Owner Name:</label>
          <input type="text" name="owner_name" required>

          <label>House Number:</label>
          <input type="text" name="house_number" required>

          <label>Location:</label>
          <input type="text" name="location" required>

          <label>Deed or Property Document:</label>
          <input type="file" name="property_doc" required>
        `;
        break;

      case 'Company':
        dynamicFields.innerHTML = `
          <label>Company Name:</label>
          <input type="text" name="company_name" required>

          <label>Registration Number:</label>
          <input type="text" name="reg_number" required>

          <label>Owner Name:</label>
          <input type="text" name="owner_name" required>

          <label>Business License:</label>
          <input type="file" name="license" required>

          <label>Tax Certificate:</label>
          <input type="file" name="tax_cert" required>
        `;
        break;

      default:
        dynamicFields.innerHTML = '';
    }
  });
});
