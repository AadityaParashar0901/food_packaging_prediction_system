# PackSmart Frontend

React + Vite + Material UI frontend for the food packaging recommendation system.

## Features

- Material Design UI
- Responsive layout
- Generous but controlled spacing
- Configurable primary/secondary palette
- Food, storage and transportation input sections
- Loading/error states
- Calls the Node backend
- Displays flexible ML recommendation output

## Setup

```bash
npm install
cp .env.example .env
npm run dev
```

The frontend expects the backend at:

`http://localhost:5000/api`

Change this with:

```env
VITE_API_URL=http://localhost:5000/api
```

## Color palette

Edit:

`src/theme.js`

```js
export const paletteConfig = {
  primary: "#1976D2",
  secondary: "#00897B",
};
```

The rest of the application uses the MUI theme, so changing these values updates the main visual palette without hunting through components.

## Backend contract

The UI calls:

`POST /api/packaging/recommend`

and sends:

```json
{
  "commodity": "tomato",
  "moisture": 94,
  "fat": 0.2,
  "pH": 4.3,
  "water_activity": 0.98,
  "respiration_rate": 25,
  "ethylene_rate": 4,
  "temperature": 10,
  "relative_humidity": 90,
  "desired_shelf_life": 14,
  "storage_type": "chilled",
  "transportation_condition": "refrigerated"
}
```

The UI intentionally doesn't assume a rigid ML response schema. Known recommendation fields are presented nicely, while additional fields from the ML server are automatically displayed too.
