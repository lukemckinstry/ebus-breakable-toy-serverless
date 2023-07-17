import { get } from "./app";

const port = process.env.PORT || 4000;

const app = get()

app.listen(port, () =>
  console.log(`Server running on port ${port}, http://localhost:${port}`)
);
