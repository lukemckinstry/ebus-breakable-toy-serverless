import { request } from "../helpers";

const payload = {
  name: "material",
  volume: 10,
  cost: 2,
  color: "#333333",
  date: "2023-07-12T13:57:00.979Z",
};

describe("Test api routes for materials", function () {
  test("a get request with empty data", async () => {
    const res = await request.get("/api/materials/");
    expect(res.header["content-type"]).toBe("application/json; charset=utf-8");
    expect(res.statusCode).toBe(200);
    expect(res.text).toEqual("[]");
  });

  test("a post request", async () => {
    const res = await request.post("/api/materials/").send(payload);
    expect(res.header["content-type"]).toBe("application/json; charset=utf-8");
    expect(res.statusCode).toBe(200);
    const { id, ...resPayload } = JSON.parse(res.text);
    expect(resPayload).toEqual(payload);
  });

  test("a get request with data", async () => {
    const res = await request.get("/api/materials/");
    expect(res.header["content-type"]).toBe("application/json; charset=utf-8");
    expect(res.statusCode).toBe(200);
    expect(JSON.parse(res.text).length).toEqual(1);
  });

  test("a put request", async () => {
    const preRes = await request.get("/api/materials/");
    const payload = JSON.parse(preRes.text)[0];
    const newPayload = {
      ...payload,
      volume: 99,
      cost: 0.99,
    };
    const res = await request.put("/api/materials/").send(newPayload);
    expect(res.header["content-type"]).toBe("application/json; charset=utf-8");
    expect(res.statusCode).toBe(200);
    expect(res.text).toEqual(JSON.stringify(payload.id));
    const postRes = await request.get("/api/materials/");
    expect(JSON.parse(postRes.text)[0]).toEqual(newPayload);
  });

  test("a delete request", async () => {
    const preRes = await request.get("/api/materials/");
    const { id } = JSON.parse(preRes.text)[0];
    const res = await request.delete(`/api/materials/${id}`);
    expect(res.header["content-type"]).toBe("application/json; charset=utf-8");
    expect(res.statusCode).toBe(200);
    expect(res.text).toEqual(JSON.stringify(id));
    const postRes = await request.get("/api/materials/");
    expect(JSON.parse(postRes.text).length).toEqual(0);
  });
});
