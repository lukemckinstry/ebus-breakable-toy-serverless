import { Request, Response } from "express";
import { datastore } from "../app";
import { v4 as uuidv4 } from "uuid";

export const listTransitRoutes = async (req: Request, res: Response) => {
  try {
    const transitRoutes = await datastore.list();
    res.json(transitRoutes);
  } catch (err) {
    res.status(500).send(err);
  }
};

export const createTransitRoute = async (req: Request, res: Response) => {
  try {
    const transitRoute = { ...req.body, id: uuidv4() };
    const newtransitRoute = await datastore.create(transitRoute);
    res.json(newtransitRoute);
  } catch (err) {
    res.status(500).send(err);
  }
};

export const deleteTransitRoute = async (req: Request, res: Response) => {
  try {
    const id = await datastore.delete(req.params.recordId);
    res.json(id);
  } catch (err) {
    res.status(500).send(err);
  }
};

// export const updatetransitRoute = async (req: Request, res: Response) => {
//   try {
//     const id = datastore.update(req.body);
//     res.json(id);
//   } catch (err) {
//     res.status(500).send(err);
//   }
// };
