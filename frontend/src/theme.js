import { createTheme } from "@mui/material/styles";

// Change these two values to re-theme the entire application.
export const paletteConfig = {
  primary: "#1976D2",
  secondary: "#00897B",
};

export const appTheme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: paletteConfig.primary,
    },
    secondary: {
      main: paletteConfig.secondary,
    },
    background: {
      default: "#F5F7FA",
      paper: "#FFFFFF",
    },
  },
  typography: {
    fontFamily:
      '"Inter", "Roboto", "Helvetica Neue", Arial, sans-serif',
    h3: {
      fontWeight: 700,
      letterSpacing: "-0.025em",
    },
    h5: {
      fontWeight: 700,
      letterSpacing: "-0.015em",
    },
    h6: {
      fontWeight: 700,
    },
  },
  shape: {
    borderRadius: 14,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          textTransform: "none",
          fontWeight: 700,
          paddingInline: 22,
          paddingBlock: 11,
        },
      },
    },
    MuiTextField: {
      defaultProps: {
        fullWidth: true,
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: "0 3px 16px rgba(20, 35, 55, 0.07)",
        },
      },
    },
  },
});
