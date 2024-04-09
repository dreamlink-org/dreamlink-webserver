import type { ColumnType } from "kysely";

export type Generated<T> = T extends ColumnType<infer S, infer I, infer U>
  ? ColumnType<S, I | undefined, U>
  : ColumnType<T, T | undefined, T>;

export type Timestamp = ColumnType<Date, Date | string, Date | string>;

export interface User {
  created_at: Timestamp;
  dream_code: string;
  handle: string;
  id: Generated<number>;
  min_jwt_iat: Timestamp;
  password: string;
}

export interface Zone {
  created_at: Timestamp;
  file_key: string;
  id: Generated<number>;
  name: string;
  updated_at: Timestamp;
  user_id: number | null;
}

export interface DB {
  user: User;
  zone: Zone;
}
