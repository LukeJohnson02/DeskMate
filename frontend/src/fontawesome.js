import { library } from "@fortawesome/fontawesome-svg-core";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { fab } from "@fortawesome/free-brands-svg-icons";

/**
 * Register the Font Awesome icon packs once at startup.
 *
 * The library registration syntax lets components refer to icons by tuple,
 * for example `["fab", "slideshare"]`, without importing that icon in every
 * component file.
 */
library.add(fas, fab);
