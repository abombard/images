import axios from "axios";
import { useItemStore } from "@/stores/items.ts";

const hostname = "http://localhost:5174";

export const search = (payload) => {
  const store = useItemStore();

  axios
    .post(
      `${hostname}/search`,
      payload,
      { headers: { "Content-Type": "application/json" } }
    )
    .then((response) => {
      if (response.data == "empty request") {
        console.log("response.data is empty");
        return;
      }

      const items = response.data.map((item) => {
        const img_prefix = "../vue"
        if (item.startsWith(img_prefix)) {
          return {
            'path': '.' + item.slice(img_prefix.length),
            'description': item,
          };
        } else {
          return {
            'description': item,
          };
        }
      });
      console.log(items);
      store.$patch({ items: items });
    })
    .catch((error) => {
      store.$patch({ errors: ["No results found", error] });
    });
}
