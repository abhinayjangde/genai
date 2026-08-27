import db from "../lib/db.js"

export const getAllUsers = async ({table})=>{

    try {
        const [rows, fields] = await db.query(`SELECT * FROM ${table}`);
        console.log("<<<<<Tools called>>>>")
        return JSON.stringify(rows);
    } catch (error) {
        console.log(error)
        return "Error while getting all users from database"
    }
}