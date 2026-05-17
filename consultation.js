const form = document.getElementById("consultation-form");
const errorEl = document.getElementById("form-error");
const successEl = document.getElementById("form-success");
const submitBtn = document.getElementById("form-submit");

const config = window.OS_CONFIG || {};
const webhookUrl = config.MAKE_WEBHOOK_URL || "";
const makeApiKey = config.MAKE_API_KEY || "";

const setStatus = (type, message) => {
  if (!errorEl || !successEl) return;
  errorEl.textContent = type === "error" ? message : "";
  successEl.textContent = type === "success" ? message : "";
};

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus("", "");

  const data = new FormData(form);

  if ((data.get("company") || "").toString().trim()) {
    return;
  }

  const interests = data
    .getAll("interest")
    .map((value) => value.toString().trim())
    .filter(Boolean);

  if (interests.length === 0) {
    setStatus("error", "Select at least one interest.");
    return;
  }

  if (!webhookUrl || !makeApiKey) {
    setStatus("error", "Form is not configured yet. Please contact support.");
    return;
  }

  const payload = {
    Time: new Date().toISOString(),
    "First Name": (data.get("firstName") || "").toString().trim(),
    "Last Name": (data.get("lastName") || "").toString().trim(),
    Email: (data.get("email") || "").toString().trim(),
    Phone: (data.get("phone") || "").toString().trim(),
    Interest: interests.join(", "),
    "Why training?": (data.get("whyTraining") || "").toString().trim(),
    "How did you find?": (data.get("howFound") || "").toString().trim(),
  };

  if (
    !payload["First Name"] ||
    !payload["Last Name"] ||
    !payload.Email ||
    !payload.Phone ||
    !payload["Why training?"] ||
    !payload["How did you find?"]
  ) {
    setStatus("error", "Please complete all required fields.");
    return;
  }

  submitBtn?.setAttribute("disabled", "true");
  submitBtn && (submitBtn.textContent = "Sending...");

  try {
    const response = await fetch(webhookUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-make-apikey": makeApiKey,
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Webhook request failed: ${response.status}`);
    }

    form.reset();
    setStatus("success", "Thanks — your consultation request was sent.");
  } catch (error) {
    setStatus("error", "Unable to submit right now. Please try again.");
  } finally {
    submitBtn?.removeAttribute("disabled");
    submitBtn && (submitBtn.textContent = "Send");
  }
});

