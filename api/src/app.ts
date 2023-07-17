import express, { Express, Request, Response } from "express";
import { routes } from "./routes";
import { TransitRoutes } from "./datastore/transitRoutes";

export const datastore = new TransitRoutes();

export const get = () => {
    const app: Express = express();

    app.use(express.json());

    // routes
    app.use("/api", routes);

    return app
}
