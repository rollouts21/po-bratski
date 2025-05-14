document.addEventListener("DOMContentLoaded", () => {
  // Система тем
  const initTheme = () => {
    const themeToggle = document.querySelector(".theme-toggle");
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    const savedTheme = localStorage.getItem("theme") || "light";

    const applyTheme = (theme) => {
      document.documentElement.setAttribute("data-theme", theme);
      metaThemeColor.content = theme === "dark" ? "#1a1a1a" : "#ffffff";
      localStorage.setItem("theme", theme);
    };

    themeToggle.addEventListener("click", () => {
      const currentTheme = document.documentElement.getAttribute("data-theme");
      const newTheme = currentTheme === "light" ? "dark" : "light";

      themeToggle.style.transform = "scale(0.8)";
      setTimeout(() => (themeToggle.style.transform = "scale(1)"), 200);
      applyTheme(newTheme);
    });

    applyTheme(savedTheme);
  };

  // Анимации при скролле
  const initScrollAnimations = () => {
    const animateElements = () => {
      document.querySelectorAll("[data-aos]").forEach((el) => {
        const rect = el.getBoundingClientRect();
        el.classList.toggle("aos-animate", rect.top < window.innerHeight * 0.8);
      });
    };

    window.addEventListener("scroll", animateElements);
    window.addEventListener("resize", animateElements);
    animateElements();
  };

  // Параллакс
  const initParallax = () => {
    const updateParallax = () => {
      document.querySelectorAll(".parallax").forEach((el) => {
        const speed = parseFloat(el.dataset.parallaxSpeed) || 0.5;
        el.style.backgroundPositionY = `${window.pageYOffset * speed}px`;
      });
    };

    window.addEventListener("scroll", updateParallax);
    updateParallax();
  };

  // Мобильное меню
  const initMobileMenu = () => {
    const menuButton = document.querySelector(".mobile-menu-btn");
    const navLinks = document.querySelector(".nav-links");

    menuButton.addEventListener("click", () => {
      navLinks.classList.toggle("active");
      menuButton.classList.toggle("active");
      document.body.classList.toggle("no-scroll");
    });
  };

  // Микроинтеракции
  const initMicroInteractions = () => {
    // Кнопки
    document.querySelectorAll(".btn-hover").forEach((btn) => {
      btn.addEventListener(
        "mouseenter",
        () => (btn.style.transform = "translateY(-2px)")
      );

      btn.addEventListener(
        "mouseleave",
        () => (btn.style.transform = "translateY(0)")
      );
    });

    // Карточки
    document.querySelectorAll(".interactive-card").forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;

        card.style.transform = `
                    perspective(1000px)
                    rotateX(${y * 8}deg)
                    rotateY(${-x * 8}deg)
                    scale(1.02)
                `;
      });

      card.addEventListener(
        "mouseleave",
        () => (card.style.transform = "none")
      );
    });

    // Кнопка корзины
    document.querySelectorAll(".add-to-cart-btn").forEach((btn) => {
      btn.addEventListener("click", function () {
        this.classList.add("added");
        setTimeout(() => this.classList.remove("added"), 2000);
      });
    });
  };

  // Инициализация всех модулей
  initTheme();
  initScrollAnimations();
  initParallax();
  initMobileMenu();
  initMicroInteractions();

  // Оптимизация скролла
  let ticking = false;
  window.addEventListener("scroll", () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        // Дополнительные операции при скролле
        ticking = false;
      });
      ticking = true;
    }
  });
});

// Добавьте в script.js
function initInfiniteCategories() {
  const grid = document.getElementById("categoriesGrid");
  const cards = grid.children;

  // Дублируем карточки для бесконечного эффекта
  const cloneCards = Array.from(cards).map((card) => card.cloneNode(true));
  cloneCards.forEach((card) => grid.appendChild(card));

  // Анимация перехода
  let isScrolling = false;

  grid.addEventListener("scroll", () => {
    if (!isScrolling) {
      window.requestAnimationFrame(() => {
        // Плавный переход
        grid.style.scrollBehavior = "smooth";

        // Сброс позиции при достижении середины
        if (grid.scrollLeft >= grid.scrollWidth / 2) {
          grid.style.scrollBehavior = "auto";
          grid.scrollLeft -= grid.scrollWidth / 2;
        }
        isScrolling = false;
      });
      isScrolling = true;
    }
  });
}

// Вызовите функцию в DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  initInfiniteCategories();
});

// Логика корзины
let cartCount = 0;

// Обновление счетчика
function updateCartCounter() {
  const counter = document.querySelector(".cart-counter");
  counter.textContent = cartCount;
  counter.style.display = cartCount > 0 ? "flex" : "none";
}

// Обработчик добавления в корзину
// document.querySelectorAll(".add-to-cart-btn").forEach((btn) => {
//   btn.addEventListener("click", () => {
//     cartCount++;
//     updateCartCounter();
//     this.style.transform = "scale(0.95)";
//     setTimeout(() => (this.style.transform = "scale(1)"), 200);

//     // Анимация иконки
//     const cart = document.querySelector(".floating-cart");
//     cart.style.transform = "scale(1.2)";
//     setTimeout(() => (cart.style.transform = "scale(1)"), 200);
//   });
// });

// // Инициализация счетчика
// updateCartCounter();
document.addEventListener("DOMContentLoaded", () => {
  const cartCounter = document.querySelector(".cart-counter");
  const cartForms = document.querySelectorAll(".add-to-cart-form");
  const CSRFToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  // Загрузка начального состояния
  const loadCartState = async () => {
    try {
      const response = await fetch('{% url "cart:cart-status" %}');
      const { total_items } = await response.json();
      cartCounter.textContent = total_items;
    } catch (error) {
      console.error("Ошибка загрузки корзины:", error);
    }
  };

  // Обработчик добавления товара
  const handleAddToCart = async (form, slug) => {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (!submitBtn) return;

    submitBtn.disabled = true;
    submitBtn.style.opacity = "0.7";

    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": CSRFToken,
        },
      });

      const data = await response.json();

      if (data.status === "success") {
        cartCounter.textContent = data.cart_total;

        // Анимация
        cartCounter.animate(
          [
            { transform: "scale(1)", opacity: 1 },
            { transform: "scale(1.5)", opacity: 0.5 },
            { transform: "scale(1)", opacity: 1 },
          ],
          500
        );
      }
    } catch (error) {
      console.error("Ошибка:", error);
    } finally {
      submitBtn.disabled = false;
      submitBtn.style.opacity = "1";
    }
  };

  // Инициализация
  loadCartState();

  // Обработчики событий
  cartForms.forEach((form) => {
    const slug = form.action.split("/").slice(-2, -1)[0];
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      handleAddToCart(form, slug);
    });
  });
});

//   function showNotification(message, type = "success") {
//     const notification = document.createElement("div");
//     notification.className = `notification ${type}`;
//     notification.textContent = message;

//     document.body.appendChild(notification);

//     setTimeout(() => {
//       notification.remove();
//     }, 3000);
//   }
// });
// Клик по корзине
// document.querySelector(".floating-cart").addEventListener("click", () => {
//   // Здесь можно добавить логику открытия корзины
//   window.location.href = "../cart.html";
// });

// Анимация стрелки при наведении
document.querySelectorAll(".view-all-btn").forEach((btn) => {
  btn.addEventListener("mouseenter", () => {
    btn.querySelector(".arrow-icon").style.transform = "translateX(5px)";
  });

  btn.addEventListener("mouseleave", () => {
    btn.querySelector(".arrow-icon").style.transform = "translateX(0)";
  });
});
