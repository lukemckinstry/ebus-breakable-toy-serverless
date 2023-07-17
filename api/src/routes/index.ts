import express from "express";
import { transitRoutes } from "./transitRoutes";

export const routes = express.Router();

routes.use("/transit", transitRoutes);
