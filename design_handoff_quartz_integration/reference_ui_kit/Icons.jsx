/* IsAbel — shared icon set.
 * Hand-picked subset of Lucide Icons (lucide.dev — ISC license),
 * inlined as React components so the UI kit works offline.
 * Stroke 2, round caps — matches the icon vocabulary IsAbel reaches for. */

const Ico = ({ d, children, size = 16, ...rest }) => (
  <svg
    width={size} height={size}
    viewBox="0 0 24 24"
    fill="none" stroke="currentColor"
    strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
    {...rest}
  >
    {d ? <path d={d}/> : children}
  </svg>
);

const Icons = {
  Search:    (p) => <Ico {...p}><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></Ico>,
  Sun:       (p) => <Ico {...p}><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></Ico>,
  Moon:      (p) => <Ico {...p}><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></Ico>,
  Chevron:   (p) => <Ico {...p}><polyline points="9 18 15 12 9 6"/></Ico>,
  ChevronDn: (p) => <Ico {...p}><polyline points="6 9 12 15 18 9"/></Ico>,
  Book:      (p) => <Ico {...p}><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></Ico>,
  Cap:       (p) => <Ico {...p}><path d="M22 10v6"/><path d="M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></Ico>,
  Mic:       (p) => <Ico {...p}><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><path d="M12 19v3"/></Ico>,
  Books:     (p) => <Ico {...p}><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></Ico>,
  Lens:      (p) => <Ico {...p}><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/><path d="M11 8v6"/><path d="M8 11h6"/></Ico>,
  Warning:   (p) => <Ico {...p}><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></Ico>,
  Bulb:      (p) => <Ico {...p}><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></Ico>,
  Folder:    (p) => <Ico {...p}><path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/></Ico>,
  File:      (p) => <Ico {...p}><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></Ico>,
  Net:       (p) => <Ico {...p}><circle cx="12" cy="12" r="3"/><circle cx="4" cy="6" r="2"/><circle cx="20" cy="6" r="2"/><circle cx="4" cy="18" r="2"/><circle cx="20" cy="18" r="2"/><path d="m6 6 6 6"/><path d="m18 6-6 6"/><path d="m6 18 6-6"/><path d="m18 18-6-6"/></Ico>,
};

window.Icons = Icons;
