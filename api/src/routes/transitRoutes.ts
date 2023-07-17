import { Router } from "express";
import {
  listTransitRoutes,
  createTransitRoute,
  deleteTransitRoute
  //updatetransitRoute,
} from "../controllers/transitRoutes";

export const transitRoutes = Router();

transitRoutes.get("/", listTransitRoutes);
transitRoutes.post("/", createTransitRoute);
transitRoutes.delete("/:recordId", deleteTransitRoute);
//transitRoutesRoutes.put("/", updateTransitRoute);
