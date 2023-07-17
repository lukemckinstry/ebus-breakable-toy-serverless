import {AttributeValue} from "@aws-sdk/client-dynamodb";


export type MaterialType = {
    id: string,
    name: string,
    volume: number,
    color: string,
    cost: number,
    delivery: string
  }


export type RouteType = {
  id: string,
  route_id: string
}