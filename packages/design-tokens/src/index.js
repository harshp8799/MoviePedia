// Design tokens shared by web (Tailwind theme) and mobile (RN styles).
// Neutral dark-first palette suited to a media-browsing UI. Values are plain JS so both
// platforms can consume them (Tailwind reads `colors`, RN reads them directly).

export const colors = {
  bg: '#0b0d12',
  surface: '#151922',
  surfaceAlt: '#1e242f',
  border: '#2a313d',
  text: '#f5f7fa',
  textMuted: '#9aa4b2',
  primary: '#e50914', // brand accent (placeholder — swap for real brand)
  primaryHover: '#c40810',
  focus: '#4c9ffe',
  success: '#2ecc71',
  warning: '#f5a623',
  danger: '#ff4d4f',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  '2xl': 48,
};

export const radii = {
  sm: 4,
  md: 8,
  lg: 12,
  pill: 999,
};

export const typography = {
  fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif",
  sizes: { xs: 12, sm: 14, base: 16, lg: 20, xl: 24, '2xl': 32, '3xl': 44 },
  weights: { regular: '400', medium: '500', semibold: '600', bold: '700' },
};

export const breakpoints = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
};
