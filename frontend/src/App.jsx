import { useMemo, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Container,
  Divider,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Snackbar,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  ThemeProvider,
  Typography,
} from "@mui/material";
import Inventory2OutlinedIcon from "@mui/icons-material/Inventory2Outlined";
import ScienceOutlinedIcon from "@mui/icons-material/ScienceOutlined";
import ThermostatOutlinedIcon from "@mui/icons-material/ThermostatOutlined";
import LocalShippingOutlinedIcon from "@mui/icons-material/LocalShippingOutlined";
import AutoAwesomeOutlinedIcon from "@mui/icons-material/AutoAwesomeOutlined";
import RefreshOutlinedIcon from "@mui/icons-material/RefreshOutlined";
import { appTheme } from "./theme";
import { getRecommendation } from "./api";
import ScrollPackagingJourney from "./components/ScrollPackagingJourney";

const initialForm = {
  commodity: "",
  moisture: "",
  fat: "",
  pH: "",
  water_activity: "",
  respiration_rate: "",
  ethylene_rate: "",
  temperature: "",
  relative_humidity: "",
  desired_shelf_life: "",
  storage_type: "ambient",
  transportation_condition: "normal",
};

function NumberField({ name, label, value, onChange, helperText, required = true }) {
  return (
    <TextField
      name={name}
      label={label}
      type="number"
      value={value}
      onChange={onChange}
      required={required}
      inputProps={{ step: "any" }}
      helperText={helperText}
    />
  );
}

function SectionHeader({ icon, title, description }) {
  return (
    <Stack direction="row" spacing={1.5} alignItems="flex-start" sx={{ mb: 3 }}>
      <Box sx={{ color: "primary.main", mt: 0.25 }}>{icon}</Box>
      <Box>
        <Typography variant="h6">{title}</Typography>
        <Typography variant="body2" color="text.secondary">
          {description}
        </Typography>
      </Box>
    </Stack>
  );
}

function RecommendationCard({ result }) {
  if (!result) return null;

  const recommendation = result.recommendation;
  if (!recommendation || typeof recommendation !== "object") return null;

  const material =
    recommendation.material ?? recommendation.packaging_material ?? "Not available";

  const thickness = recommendation.thickness;
  const otr = recommendation.otr;
  const wvtr = recommendation.wvtr;
  const map = recommendation.map;
  const mechanical = recommendation.mechanical_strength;

  const shortValue = (value, unit = "") => {
    if (value === undefined || value === null || value === "") return "Not available";
    if (typeof value !== "object") return `${value}${unit}`;
    if ("value" in value) return `${value.value} ${value.unit ?? unit}`.trim();
    if ("requirement_score" in value) return `${value.requirement_score} score`;
    if ("suitable" in value) return value.suitable ? "Yes" : "No";
    if ("score" in value) return `${value.score} score`;
    return "Available";
  };

  const rows = [
    ["Recommended material", material],
    ["Film thickness", shortValue(thickness)],
    ["OTR requirement", shortValue(otr)],
    ["WVTR requirement", shortValue(wvtr)],
    ["Sealability", recommendation.sealability ?? "Not available"],
    ["MAP suitability", shortValue(map)],
    ["Mechanical strength", shortValue(mechanical)],
  ];

  return (
    <Card sx={{ mt: 4 }}>
      <CardContent sx={{ p: { xs: 2, md: 3 } }}>
        <SectionHeader
          icon={<AutoAwesomeOutlinedIcon />}
          title="Packaging recommendation"
          description="Short summary of the model output."
        />

        <TableContainer
          component={Box}
          sx={{
            border: "1px solid",
            borderColor: "divider",
            borderRadius: 2,
            overflow: "hidden",
          }}
        >
          <Table size="small">
            <TableHead>
              <TableRow sx={{ bgcolor: "grey.50" }}>
                <TableCell sx={{ fontWeight: 700 }}>Parameter</TableCell>
                <TableCell sx={{ fontWeight: 700 }}>Recommendation</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map(([label, value]) => (
                <TableRow key={label}>
                  <TableCell sx={{ color: "text.secondary", width: "48%" }}>
                    {label}
                  </TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>{value}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        {recommendation.prototype && (
          <Typography
            variant="caption"
            color="text.secondary"
            sx={{ display: "block", mt: 1.5 }}
          >
            Prototype estimates using synthetic training data.
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}

export default function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const canSubmit = useMemo(
    () =>
      form.commodity.trim() &&
      Object.entries(form).every(([key, value]) => {
        if (key === "commodity" || key === "storage_type" || key === "transportation_condition") {
          return value !== "";
        }
        return value !== "";
      }),
    [form]
  );

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  function resetForm() {
    setForm(initialForm);
    setResult(null);
    setError("");
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    const payload = {
      ...form,
      moisture: Number(form.moisture),
      fat: Number(form.fat),
      pH: Number(form.pH),
      water_activity: Number(form.water_activity),
      respiration_rate: Number(form.respiration_rate),
      ethylene_rate: Number(form.ethylene_rate),
      temperature: Number(form.temperature),
      relative_humidity: Number(form.relative_humidity),
      desired_shelf_life: Number(form.desired_shelf_life),
    };

    try {
      const data = await getRecommendation(payload);
      setResult(data);
      window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <ThemeProvider theme={appTheme}>
      <Box sx={{ minHeight: "100vh", bgcolor: "background.default" }}>
        <Box
          sx={{
            bgcolor: "primary.main",
            color: "primary.contrastText",
            py: { xs: 4, md: 5 },
          }}
        >
          <Container maxWidth="lg">
            <Stack direction="row" spacing={2} alignItems="center">
              <Inventory2OutlinedIcon sx={{ fontSize: 40 }} />
              <Box>
                <Typography variant="h3" sx={{ fontSize: { xs: "2rem", md: "2.7rem" } }}>
                  PackSmart
                </Typography>
                <Typography sx={{ opacity: 0.88, mt: 0.5 }}>
                  Intelligent food packaging recommendation
                </Typography>
              </Box>
            </Stack>
          </Container>
        </Box>

        <ScrollPackagingJourney />

        <Container id="food-storage-profile" maxWidth="lg" sx={{ py: { xs: 4, md: 6 } }}>
          <Box sx={{ maxWidth: 980, mx: "auto" }}>
            <Box sx={{ mb: 4 }}>
              <Typography variant="h5">Food & storage profile</Typography>
              <Typography color="text.secondary" sx={{ mt: 0.75 }}>
                Enter the product and environmental conditions to generate a packaging recommendation.
              </Typography>
            </Box>

            <form onSubmit={handleSubmit}>
              <Card>
                <CardContent sx={{ p: { xs: 3, md: 4.5 } }}>
                  <SectionHeader
                    icon={<ScienceOutlinedIcon />}
                    title="Food properties"
                    description="These values describe the commodity being packaged."
                  />

                  <Grid container spacing={2.5}>
                    <Grid size={{ xs: 12, sm: 6 }}>
                      <TextField
                        name="commodity"
                        label="Commodity"
                        value={form.commodity}
                        onChange={handleChange}
                        placeholder="e.g. tomato"
                        required
                      />
                    </Grid>

                    <Grid size={{ xs: 12, sm: 6 }}>
                      <NumberField
                        name="moisture"
                        label="Moisture (%)"
                        value={form.moisture}
                        onChange={handleChange}
                      />
                    </Grid>

                    <Grid size={{ xs: 12, sm: 6 }}>
                      <NumberField
                        name="fat"
                        label="Fat (%)"
                        value={form.fat}
                        onChange={handleChange}
                      />
                    </Grid>

                    <Grid size={{ xs: 12, sm: 6 }}>
                      <NumberField
                        name="pH"
                        label="pH"
                        value={form.pH}
                        onChange={handleChange}
                      />
                    </Grid>

                    <Grid size={{ xs: 12, sm: 6 }}>
                      <NumberField
                        name="water_activity"
                        label="Water activity (aw)"
                        value={form.water_activity}
                        onChange={handleChange}
                        helperText="Usually between 0 and 1"
                      />
                    </Grid>

                    <Grid size={{ xs: 12, sm: 6 }}>
                      <NumberField
                        name="respiration_rate"
                        label="Respiration rate"
                        value={form.respiration_rate}
                        onChange={handleChange}
                        helperText="Use your chosen dataset unit"
                      />
                    </Grid>

                    <Grid size={{ xs: 12, sm: 6 }}>
                      <NumberField
                        name="ethylene_rate"
                        label="Ethylene rate"
                        value={form.ethylene_rate}
                        onChange={handleChange}
                        helperText="Use your chosen dataset unit"
                      />
                    </Grid>
                  </Grid>

                  <Divider sx={{ my: 4 }} />

                  <SectionHeader
                    icon={<ThermostatOutlinedIcon />}
                    title="Storage conditions"
                    description="Environmental conditions strongly affect shelf life and barrier requirements."
                  />

                  <Grid container spacing={2.5}>
                    <Grid size={{ xs: 12, sm: 6 }}>
                      <NumberField
                        name="temperature"
                        label="Storage temperature (°C)"
                        value={form.temperature}
                        onChange={handleChange}
                      />
                    </Grid>

                    <Grid size={{ xs: 12, sm: 6 }}>
                      <NumberField
                        name="relative_humidity"
                        label="Relative humidity (%)"
                        value={form.relative_humidity}
                        onChange={handleChange}
                      />
                    </Grid>

                    <Grid size={{ xs: 12, sm: 6 }}>
                      <NumberField
                        name="desired_shelf_life"
                        label="Desired shelf life (days)"
                        value={form.desired_shelf_life}
                        onChange={handleChange}
                      />
                    </Grid>

                    <Grid size={{ xs: 12, sm: 6 }}>
                      <FormControl fullWidth>
                        <InputLabel>Storage type</InputLabel>
                        <Select
                          name="storage_type"
                          value={form.storage_type}
                          label="Storage type"
                          onChange={handleChange}
                        >
                          <MenuItem value="ambient">Ambient</MenuItem>
                          <MenuItem value="chilled">Chilled</MenuItem>
                          <MenuItem value="frozen">Frozen</MenuItem>
                        </Select>
                      </FormControl>
                    </Grid>
                  </Grid>

                  <Divider sx={{ my: 4 }} />

                  <SectionHeader
                    icon={<LocalShippingOutlinedIcon />}
                    title="Transportation"
                    description="Account for the environment the package must survive outside storage."
                  />

                  <Grid container spacing={2.5}>
                    <Grid size={{ xs: 12, sm: 6 }}>
                      <FormControl fullWidth>
                        <InputLabel>Transportation condition</InputLabel>
                        <Select
                          name="transportation_condition"
                          value={form.transportation_condition}
                          label="Transportation condition"
                          onChange={handleChange}
                        >
                          <MenuItem value="normal">Normal</MenuItem>
                          <MenuItem value="refrigerated">Refrigerated</MenuItem>
                          <MenuItem value="frozen">Frozen</MenuItem>
                        </Select>
                      </FormControl>
                    </Grid>
                  </Grid>

                  <Stack
                    direction={{ xs: "column", sm: "row" }}
                    spacing={1.5}
                    justifyContent="flex-end"
                    sx={{ mt: 4 }}
                  >
                    <Button
                      type="button"
                      variant="outlined"
                      startIcon={<RefreshOutlinedIcon />}
                      onClick={resetForm}
                      disabled={loading}
                    >
                      Reset
                    </Button>
                    <Button
                      type="submit"
                      variant="contained"
                      startIcon={
                        loading ? <CircularProgress size={18} color="inherit" /> : <AutoAwesomeOutlinedIcon />
                      }
                      disabled={!canSubmit || loading}
                    >
                      {loading ? "Analyzing..." : "Get recommendation"}
                    </Button>
                  </Stack>
                </CardContent>
              </Card>
            </form>

            {result && <RecommendationCard result={result} />}

            <Box sx={{ mt: 4, textAlign: "center" }}>
              <Chip
                label="ML-powered decision support"
                variant="outlined"
                color="primary"
                size="small"
              />
            </Box>
          </Box>
        </Container>

        <Snackbar
          open={Boolean(error)}
          autoHideDuration={7000}
          onClose={() => setError("")}
          anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
        >
          <Alert severity="error" onClose={() => setError("")} variant="filled">
            {error}
          </Alert>
        </Snackbar>
      </Box>
    </ThemeProvider>
  );
}
