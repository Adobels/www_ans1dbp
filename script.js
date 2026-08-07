const year = document.querySelector("[data-year]");

if (year) {
  year.textContent = new Date().getFullYear();
}

const boardMembersElectedOnApril26 = [
  { initials: "JR", role: "Président d'Honneur", name: "Jean-Pierre RUAULT" },
  { initials: "BS", role: "Président", name: "Blazej SLEBODA" },
  { initials: "AR", role: "Vice-Présidente - Relations polonaises et européennes", name: "Anne ROUVIERE" },
  { initials: "CV", role: "Vice-Présidente - Relations françaises", name: "Christèle VILLETTE" },
  { initials: "DC", role: "Secrétaire Général", name: "Damien CIERPISZ" },
  { initials: "TB", role: "Trésorier et Maître de cérémonies", name: "Thierry BERTIN" },
  { initials: "GL", role: "Secrétaire Adjoint et Responsable publication Facebook", name: "Guillaume de LOUVENCOURT" },
  { initials: "PD", role: "Porte-drapeau", name: "Pascal DUHAMEAU" },
  { initials: "RB", role: "Porte-drapeau Adjoint", name: "Rafał BURKAT" },
];

const boardVersions = {
  "2026-08-04": {
    title: "Composition du conseil d'administration depuis le 4 août 2026.",
    description: "",
    note: "",
    members: boardMembersElectedOnApril26.filter((member) => member.name !== "Rafał BURKAT"),
  },
  "2026-04-26": {
    title: "Membres élus le 26 avril 2026.",
    description: "Composition issue de l'assemblée générale du 26 avril 2026.",
    note: "Cette version présente le conseil d'administration tel qu'il a été élu le 26 avril 2026.",
    eventsTitle: "Événement ayant provoqué la version suivante",
    events: [
      {
        date: "4 août 2026",
        text: "Démission de Rafał BURKAT. À partir de cette date, il ne fait plus partie du conseil d'administration.",
      },
    ],
    members: boardMembersElectedOnApril26,
  },
};

const boardGrid = document.querySelector("[data-board-grid]");
const boardTitle = document.querySelector("[data-board-title]");
const boardDescription = document.querySelector("[data-board-description]");
const boardNote = document.querySelector("[data-board-note]");
const boardEvents = document.querySelector("[data-board-events]");
const boardVersionButtons = document.querySelectorAll("[data-board-version-button]");

const createBoardCard = ({ initials, role, name }) => {
  const card = document.createElement("article");
  card.className = "person-card reveal is-visible";

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = initials;

  const roleElement = document.createElement("p");
  roleElement.textContent = role;

  const nameElement = document.createElement("h3");
  nameElement.textContent = name;

  card.append(avatar, roleElement, nameElement);
  return card;
};

const createBoardEvents = ({ eventsTitle, events }) => {
  if (!events || events.length === 0) {
    return [];
  }

  const title = document.createElement("h3");
  title.textContent = eventsTitle;

  const list = document.createElement("ul");

  events.forEach((event) => {
    const item = document.createElement("li");
    const date = document.createElement("strong");
    date.textContent = event.date;
    const text = document.createTextNode(` - ${event.text}`);

    item.append(date, text);
    list.append(item);
  });

  return [title, list];
};

const renderBoardVersion = (versionKey) => {
  const version = boardVersions[versionKey];

  if (!version || !boardGrid || !boardTitle || !boardDescription || !boardNote || !boardEvents) {
    return;
  }

  boardTitle.textContent = version.title;
  boardDescription.textContent = version.description;
  boardDescription.hidden = !version.description;
  boardNote.textContent = version.note;
  boardNote.hidden = !version.note;
  boardGrid.replaceChildren(...version.members.map(createBoardCard));
  boardEvents.replaceChildren(...createBoardEvents(version));
  boardEvents.hidden = !version.events || version.events.length === 0;

  boardVersionButtons.forEach((button) => {
    const isActive = button.dataset.boardVersionButton === versionKey;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });
};

boardVersionButtons.forEach((button) => {
  button.addEventListener("click", () => {
    renderBoardVersion(button.dataset.boardVersionButton);
  });
});

renderBoardVersion("2026-08-04");

const revealItems = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.14 }
  );

  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}
