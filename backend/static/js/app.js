// Omah Rias Ika — Alpine.js Application

document.addEventListener("alpine:init", () => {
  // Global store for app state
  Alpine.store("app", {
    mobileMenuOpen: false,
    currentPage: "home",

    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen;
    },
  });

  // Multi-step booking form component
  Alpine.data("bookingForm", () => ({
    currentStep: 1,
    totalSteps: 4,
    formData: {
      // Step 1: Contact Details
      name: "",
      whatsapp: "",

      // Step 2: Event Details
      eventDate: "",
      venue: "",
      guestCount: "",

      // Step 3: Service Selection
      selectedPackage: "",
      addOns: [],

      // Step 4: Notes
      notes: "",
    },
    errors: {},
    isSubmitting: false,

    init() {
      const params = new URLSearchParams(window.location.search);
      const pkg = params.get("package");
      if (pkg && ["basic", "medium", "extra", "custom"].includes(pkg)) {
        this.formData.selectedPackage = pkg;
      }
    },

    validateStep(step) {
      this.errors = {};

      if (step === 1) {
        if (!this.formData.name.trim()) {
          this.errors.name = "Nama lengkap wajib diisi";
        }
        if (!this.formData.whatsapp.trim()) {
          this.errors.whatsapp = "Nomor WhatsApp wajib diisi";
        } else if (
          !/^62\d{9,12}$/.test(this.formData.whatsapp.replace(/\D/g, ""))
        ) {
          this.errors.whatsapp = "Format: 628xxxxxxxxxx";
        }
      }

      if (step === 2) {
        if (!this.formData.eventDate) {
          this.errors.eventDate = "Tanggal acara wajib diisi";
        }
        if (!this.formData.venue.trim()) {
          this.errors.venue = "Lokasi venue wajib diisi";
        }
        if (!this.formData.guestCount) {
          this.errors.guestCount = "Perkiraan jumlah tamu wajib diisi";
        }
      }

      if (step === 3) {
        if (!this.formData.selectedPackage) {
          this.errors.selectedPackage = "Pilih salah satu paket";
        }
      }

      return Object.keys(this.errors).length === 0;
    },

    nextStep() {
      if (this.validateStep(this.currentStep)) {
        if (this.currentStep < this.totalSteps) {
          this.currentStep++;
        }
      }
    },

    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
      }
    },

    async submitForm() {
      if (!this.validateStep(this.currentStep)) return;

      this.isSubmitting = true;

      try {
        const response = await fetch("/api/booking/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: this.formData.name,
            whatsapp: this.formData.whatsapp,
            event_date: this.formData.eventDate,
            venue: this.formData.venue,
            guest_count: this.formData.guestCount,
            package: this.formData.selectedPackage,
            notes: this.formData.notes,
          }),
        });
        const result = await response.json();

        if (result.success) {
          sessionStorage.setItem(
            "bookingData",
            JSON.stringify({
              ...this.formData,
              bookingCode: result.booking_code,
              submittedAt: new Date().toISOString(),
            }),
          );
          window.location.href = "/booking/success/";
        } else {
          alert("Error: " + result.error);
        }
      } catch (err) {
        alert("Failed to connect to server.");
      } finally {
        this.isSubmitting = false;
      }
    },

    get progress() {
      return (this.currentStep / this.totalSteps) * 100;
    },
  }));

  // Catalog filter component
  Alpine.data("catalogFilter", () => ({
    activeCategory: "all",
    init() {
      const params = new URLSearchParams(window.location.search);
      const cat = params.get("category");
      if (cat && this.categories.some((c) => c.id === cat)) {
        this.activeCategory = cat;
      }
    },
    categories: [
      { id: "all", name: "Semua", iconPath: "/static/assets/icon/star.png" },
      {
        id: "mua",
        name: "MUA",
        iconPath: "/static/assets/icon/cosmetics.png",
      },
      {
        id: "decoration",
        name: "Dekorasi",
        iconPath: "/static/assets/icon/decoration.png",
      },
      {
        id: "tent",
        name: "Tenda",
        iconPath: "/static/assets/icon/marquee.png",
      },
      {
        id: "catering",
        name: "Katering",
        iconPath: "/static/assets/icon/buffet.png",
      },
      {
        id: "photographer",
        name: "Fotografer",
        iconPath: "/static/assets/icon/photographer.png",
      },
      {
        id: "music",
        name: "Musik",
        iconPath: "/static/assets/icon/music.png",
      },
      {
        id: "invitation",
        name: "Undangan",
        iconPath: "/static/assets/icon/invitation.png",
      },
      {
        id: "gift",
        name: "Hantaran",
        iconPath: "/static/assets/icon/gift.png",
      },
    ],

    setCategory(categoryId) {
      this.activeCategory = categoryId;
    },

    isVisible(itemCategory) {
      return (
        this.activeCategory === "all" || this.activeCategory === itemCategory
      );
    },
  }));

  // Booking check component
  Alpine.data("bookingCheck", () => ({
    whatsapp: "",
    bookingCode: "",
    isLoading: false,
    showModal: false,
    bookingData: null,
    error: "",

    async checkBooking() {
      this.error = "";

      if (!this.whatsapp.trim() || !this.bookingCode.trim()) {
        this.error = "Mohon isi nomor WhatsApp dan kode booking";
        return;
      }

      this.isLoading = true;

      try {
        const response = await fetch("/api/booking/check/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            whatsapp: this.whatsapp.replace(/\D/g, ""),
            code: this.bookingCode.trim().toUpperCase(),
          }),
        });
        const result = await response.json();

        if (result.success) {
          const b = result.booking;
          const progressMap = {
            completed: 100,
            ready: 90,
            technical_meeting: 60,
            dp: 30,
            booking: 10,
          };
          this.bookingData = {
            whatsapp: this.whatsapp.replace(/\D/g, ""),
            name: b.name,
            status: b.status,
            statusLabel: b.status_display,
            package: b.package,
            eventDate: b.event_date,
            venue: b.venue,
            totalAmount: b.total_amount,
            paidAmount: b.paid_amount,
            progress: progressMap[b.status] || 10,
          };
          this.showModal = true;
        } else {
          this.error =
            "Data tidak ditemukan. Pastikan nomor WhatsApp dan kode booking benar.";
        }
      } catch (err) {
        this.error = "Gagal terhubung ke server.";
      } finally {
        this.isLoading = false;
      }
    },

    closeModal() {
      this.showModal = false;
      this.bookingData = null;
    },

    handleKeydown(event) {
      if (event.key === "Escape" && this.showModal) {
        this.closeModal();
      }
    },

    formatCurrency(amount) {
      return new Intl.NumberFormat("id-ID", {
        style: "currency",
        currency: "IDR",
        minimumFractionDigits: 0,
      }).format(amount);
    },

    get statusSteps() {
      const steps = [
        { id: "booking", label: "Booking", icon: "📋" },
        { id: "dp", label: "Down Payment", icon: "💰" },
        { id: "technical_meeting", label: "Technical Meeting", icon: "🤝" },
        { id: "ready", label: "Ready", icon: "✅" },
      ];

      const currentIndex = steps.findIndex(
        (s) => s.id === this.bookingData?.status,
      );
      return steps.map((step, index) => ({
        ...step,
        completed: index < currentIndex,
        current: index === currentIndex,
      }));
    },
  }));

  // Package selection component
  Alpine.data("packageSelector", () => ({
    packages: [
      {
        id: "basic",
        name: "Basic",
        price: 25000000,
        description: "Paket dasar untuk pernikahan intimate",
        features: [
          "Dekorasi Pelaminan Standar",
          "MUA untuk Bride",
          "Dokumentasi Foto (1 Fotografer)",
          "Catering 100 pax",
          "Sound System Basic",
        ],
        notIncluded: ["Tenda", "Videografi", "Live Music"],
      },
      {
        id: "medium",
        name: "Medium",
        price: 50000000,
        description: "Paket lengkap untuk pernikahan menengah",
        features: [
          "Dekorasi Pelaminan Premium",
          "MUA untuk Bride & Groom",
          "Dokumentasi Foto (2 Fotografer)",
          "Dokumentasi Video",
          "Catering 200 pax",
          "Sound System + MC",
          "Tenda 10x10m",
        ],
        notIncluded: ["Live Music", "Photo Booth"],
      },
      {
        id: "extra",
        name: "Extra",
        price: 75000000,
        popular: true,
        description: "Paket premium untuk pernikahan impian",
        features: [
          "Dekorasi Pelaminan Mewah",
          "MUA Premium (Bride, Groom, Keluarga)",
          "Dokumentasi Foto (3 Fotografer)",
          "Dokumentasi Video Cinematic",
          "Catering 300 pax",
          "Sound System Premium + MC Pro",
          "Tenda 15x15m dengan AC",
          "Live Acoustic Band",
          "Photo Booth",
        ],
        notIncluded: [],
      },
      {
        id: "custom",
        name: "Custom",
        price: null,
        description: "Sesuaikan paket dengan kebutuhan Anda",
        features: [
          "Konsultasi Gratis",
          "Pilih Vendor Sendiri",
          "Fleksibel Budget",
          "Personal Wedding Planner",
          "Negosiasi Langsung",
        ],
        notIncluded: [],
      },
    ],

    formatPrice(price) {
      if (!price) return "Hubungi Kami";
      return new Intl.NumberFormat("id-ID", {
        style: "currency",
        currency: "IDR",
        minimumFractionDigits: 0,
      }).format(price);
    },
  }));
});

// Helper function to format phone number
function formatPhoneNumber(input) {
  let value = input.value.replace(/\D/g, "");
  if (!value.startsWith("62")) {
    if (value.startsWith("0")) {
      value = "62" + value.substring(1);
    } else {
      value = "62" + value;
    }
  }
  input.value = value;
}

// Smooth scroll to element
function scrollToElement(elementId) {
  const element = document.getElementById(elementId);
  if (element) {
    element.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}
