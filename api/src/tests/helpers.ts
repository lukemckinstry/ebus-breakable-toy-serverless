
import { agent as _request } from "supertest"
import {get as getApplication} from '../app'

export const request = _request(getApplication())