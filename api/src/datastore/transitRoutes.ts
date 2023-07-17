import {
  DynamoDBClient,
  ScanCommand,
  PutItemCommand,
  DeleteItemCommand,
} from "@aws-sdk/client-dynamodb";

import { RouteType } from "../utils/models";

const dynamodb = new DynamoDBClient({
  region: "us-east-1",
  endpoint: "http://dynamodb:8000/",
  credentials: {
    accessKeyId: "xxx",
    secretAccessKey: "yyy",
  },
});

const ROUTE_TABLE = "routes";

export class TransitRoutes {
  constructor() {}

  async list() {
    const params = {
      TableName: ROUTE_TABLE,
    };
    const routes = await dynamodb.send(new ScanCommand(params));
    return routes;
  }

  async create(route: RouteType) {
    const item = Object.fromEntries(Object.entries(route).map(([k,v])=>[k, {"S": v}]))
    const params = {
      "Item": item,
      "ReturnConsumedCapacity": "TOTAL",
      "TableName": ROUTE_TABLE
    };    
    return await dynamodb.send(new PutItemCommand(params));
  }

  async delete(id: string) {
    const params = {
      TableName: ROUTE_TABLE,
      Key: {
        id: {
          S: id,
        },
      },
    };

    return await dynamodb.send(new DeleteItemCommand(params));
  }

  // update(newMaterial: MaterialType) {
  //   const id = newMaterial.id;
  //   const newArray = this.materials.filter((a) => a.id != id);
  //   this.materials = newArray;
  //   this.materials.push(newMaterial);
  //   return id;
  // }
}
